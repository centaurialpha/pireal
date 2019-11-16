# -*- coding: utf-8 -*-
#
# Copyright 2015-2016 - Gabriel Acosta <acostadariogabriel@gmail.com>
#
# This file is part of Pireal.
#
# Pireal is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Pireal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pireal; If not, see <http://www.gnu.org/licenses/>.

from collections import OrderedDict

from pireal.core.interpreter.tokens import (
    STRING,
    DATE,
    TIME,
    SEMICOLON,
    INTEGER,
    REAL,
    ID,
    LPAREN,
    RPAREN,
    SEMI,
    SELECT,
    PROJECT,
    BINARYOP,
    EQUAL,
    NOTEQUAL,
    LESS,
    GREATER,
    LEQUAL,
    GEQUAL,
    KEYWORDS,
    AND,
    OR,
    ASSIGNMENT,
    EOF
)
from pireal.core.interpreter.exceptions import ConsumeError
from pireal.core.interpreter.exceptions import DuplicateRelationNameError

from pireal.core.interpreter import scanner
from pireal.core.interpreter import lexer
from pireal.core.interpreter import rast as ast


class Parser(object):
    """ The Parser is the part that really understands the syntax of
    the language. It calls the Lexer to get tokens and processes the tokens
    per the syntax of the language.
    """

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = self.lexer.next_token()

    def consume(self, token_type):
        """ Consume a token of a given type and get the next token.
        If the current token is not of the expected type, then
        raise an error
        """

        if self.token.type == token_type:
            self.token = self.lexer.next_token()
        else:
            raise ConsumeError(
                token_type,
                self.token.type,
                self.lexer.sc.lineno
            )

    def parse(self):
        """
        Compound : Assignment
                 | Assignment; Compound

        Assignment : RNAME := Expression;

        Expression : SELECT Condition (Expression)
                   | PROJECT AttrList (Expression)
                   | Expression NJOIN Expression
                   | Expression PRODUCT Expression
                   | Expression INTERSECT Expression
                   | Expression UNION Expression
                   | Expression DIFFERENCE Expression
                   | (Expression)
                   | NAME

        AttrList : NAME
                 | NAME, AttrsList

        Condition : Compared Comp Compared
                  | (Condition)
                  | Condition AND Condition
                  | Condition OR Condition

        Compared : ATTRIBUTE
                 | Data

        Comp : =
             | <>
             | <
             | >
             | <=
             | >=

        Data : NUMBER
             | STRING
        """

        node = self._compound()
        return node

    def _compound(self):
        """
        Compound : Assignment
                 | Assignment; Compound
        """

        nodes = []

        while self.token.type != EOF:
            nodes.append(self._assignment())

        compound = ast.Compound()
        compound.children = nodes

        return compound

    def _assignment(self):
        """
        Assignment : RNAME := Expression;
        """

        rname = ast.Variable(self.token)
        self.consume(ID)
        self.consume(ASSIGNMENT)
        q = self._expression()
        node = ast.Assignment(rname, q)
        self.consume(SEMICOLON)

        return node

    def _binary_expression(self, left_node):
        """
        BinaryExpression : (Expression) BinaryOp (Expression)
        """

        operator = self.token
        self.consume(KEYWORDS.get(operator.value))
        right_node = self._expression()
        return ast.BinaryOp(left_node, operator, right_node)

    def _variable(self):
        node = ast.Variable(self.token)
        self.consume(ID)
        return node

    def _project_expression(self):
        """
        ProjectExpression : PROJECT AttrList (Expression)
        """

        self.consume(PROJECT)
        attributes = self._attributes()
        self.consume(LPAREN)
        expression = self._expression()
        self.consume(RPAREN)
        return ast.ProjectExpr(attributes, expression)

    def _select_expression(self):
        """
        SelectExpression : SELECT Condition (Expression)
        """

        self.consume(SELECT)
        condition = self._condition()
        # Bool operation
        bool_op = None
        if self.token.type in (AND, OR):
            bool_op = ast.BoolOp()
            bool_op.conditions.append(condition)

            while self.token.type in (AND, OR):
                op = self.token.value
                self.consume(KEYWORDS.get(op))
                bool_op.ops.append(op)
                bool_op.conditions.append(self._condition())

        if bool_op is not None:
            condition = bool_op
        # FIXME: puede venir otra CONDITION
        self.consume(LPAREN)
        expression = self._expression()
        self.consume(RPAREN)
        return ast.SelectExpr(condition, expression)

    def _expression(self):
        """
        Expression : SelectExpression
                   | ProjectExpression
                   | (Expression)
                   | BinaryExpression
                   | NAME
        """

        # Select
        if self.token.type == SELECT:
            node = self._select_expression()

        # Project
        elif self.token.type == PROJECT:
            node = self._project_expression()

        # (Expression) or (Expression) BinaryOp (Expression)
        elif self.token.type == LPAREN:
            self.consume(LPAREN)
            node = self._expression()
            self.consume(RPAREN)
            # If next token is binary operator, them create BinaryOp node
            if self.token.type in BINARYOP:
                # Pass the left node
                node = self._binary_expression(node)

        # Var
        elif self.token.type == ID:
            node = self._variable()
            if self.token.type in BINARYOP:
                # Pass the left node
                node = self._binary_expression(node)
        else:
            self.consume("EXPRESSION")
        return node

    def _condition(self):
        """
        Condition : Compared Comp Compared
                  | (Condition)
        """

        if self.token.type == LPAREN:
            self.consume(LPAREN)
            node = self._condition()
            self.consume(RPAREN)
        elif self.token.type == ID:
            compared = self._compared()
            comp = self._comp()
            compared2 = self._compared()
            node = ast.Condition(compared, comp, compared2)
        else:
            self.consume("CONDITION")

        return node

    def _comp(self):
        """
        Comp : =
             | <>
             | <
             | >
             | <=
             | >=
        """

        node = self.token

        if self.token.type == EQUAL:
            self.consume(EQUAL)
        elif self.token.type == NOTEQUAL:
            self.consume(NOTEQUAL)
        elif self.token.type == LESS:
            self.consume(LESS)
        elif self.token.type == GREATER:
            self.consume(GREATER)
        elif self.token.type == LEQUAL:
            self.consume(LEQUAL)
        elif self.token.type == GEQUAL:
            self.consume(GEQUAL)
        else:
            self.consume('COMPARATOR')

        return node

    def _compared(self):
        """
        Compared : ATTRIBUTE
                 | Data
        """

        if self.token.type == ID:
            node = ast.Variable(self.token)
            self.consume(ID)
        else:
            node = self._data()

        return node

    def _data(self):
        """
        Data : INTEGER
             | REAL
             | DATE
             | TIME
             | STRING
        """

        if self.token.type == INTEGER:
            node = ast.Number(self.token)
            self.consume(INTEGER)
        elif self.token.type == REAL:
            node = ast.Number(self.token)
            self.consume(REAL)
        elif self.token.type == DATE:
            node = ast.Date(self.token)
            self.consume(DATE)
        elif self.token.type == TIME:
            node = ast.Time(self.token)
            self.consume(TIME)
        elif self.token.type == STRING:
            node = ast.String(self.token)
            self.consume(STRING)
        else:
            self.consume("CONSTANT")

        return node

    def _attributes(self):
        """
        AttrList : NAME
                 | NAME, AttrsList
        """

        node = ast.Variable(self.token)
        self.consume(ID)

        results = [node]

        while self.token.type == SEMI:
            self.consume(SEMI)
            results.append(ast.Variable(self.token))
            self.consume(ID)

        return results


class Interpreter(ast.NodeVisitor):
    """ Este objeto es el encargado de 'visitar' los nodos con el
    método Interpreter.to_python(), que convierte a un string que luego
    es evaluado como código Python

    El scope es un diccionario ordenado que guarda las consultas 'reales'
    que serán evaluadas
    """

    # key: relation_name
    # value: query
    SCOPE = OrderedDict()

    def __init__(self, parser):
        self.parser = parser

    def to_python(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assignment(self, node):
        rname = self.visit(node.rname)
        if rname in self.SCOPE:
            raise DuplicateRelationNameError(rname)
        self.SCOPE[rname] = self.visit(node.query)

    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return '{0}.{1}({2})'.format(
            left,
            node.token.value,
            right
        )

    def visit_Number(self, node):
        return node.num

    def visit_ProjectExpr(self, node):
        attrs = [i.value for i in node.attrs]
        expr = self.visit(node.expr)
        return '{0}.project({1})'.format(
            expr,
            ', '.join("'{0}'".format(i) for i in attrs)
        )

    def visit_SelectExpr(self, node):
        cond = self.visit(node.condition)
        expr = self.visit(node.expr)

        return '{0}.select("{1}")'.format(
            expr,
            cond
        )

    def visit_BoolOp(self, node):
        conditions = " \"{}\" ".join([self.visit(c) for c in node.conditions])
        return conditions.format(*node.ops).replace("\"", '')

    def visit_Condition(self, node):
        op1 = self.visit(node.op1)
        op2 = self.visit(node.op2)
        operator = node.operator.value
        if operator == '=':
            operator += '='
        if operator == '<>':
            operator = '!='

        return '{0} {1} {2}'.format(
            op1,
            operator,
            op2
        )

    def visit_Variable(self, node):
        return node.value

    def visit_Date(self, node):
        return repr(node.date)

    def visit_Time(self, node):
        return repr(node.time)

    def visit_String(self, node):
        return repr(node.string)

    def clear(self):
        self.SCOPE.clear()


def parse(query):
    sc = scanner.Scanner(query)
    lex = lexer.Lexer(sc)
    parser = Parser(lex)
    interpreter = Interpreter(parser)
    interpreter.clear()
    interpreter.to_python()
    return interpreter.SCOPE
