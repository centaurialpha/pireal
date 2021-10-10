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
"""
<Compound>          : <Query>
                    | <Query> <Compund>
<Query>             : <Assignment> SEMI
<Assignment>        : <Variable> ASSIGNMENT <Expression>
<Expression>        : <Variable>
                    | LPAREN <Expression> RPAREN
                    | <SelectExpression>
                    | <ProjectExpression>
                    | <BinaryExpression>
<SelectExpression>  : SELECT <BooleanExpression> LPAREN <Expression> RPAREN
<ProjectExpression> : PROJECT <AttributeList> LPAREN <Expression> RPAREN
<BinaryExpression>  : <Expression> NJOIN <Expression>
                    | <Expression> LOUTER <Expression>
                    | <Expression> ROUTER <Expression>
                    | <Expression> FOUTER <Expression>
                    | <Expression> PRODUCT <Expression>
                    | <Expression> DIFFERENCE <Expression>
                    | <Expression> INTERSECT <Expression>
                    | <Expression> UNION <Expression>
<BooleanExpression> : <Formula>
                    | <Formula> AND <Formula>
                    | <Formula> OR <Formula>
<AttributeList>     : <Variable>
                    | <Variable> COMMA <AttributeList>
<Formula>           : <Operand> <Operator> <Operand>
<Operand>           : <Variable>
                    | <Literal>
<Operator>          : EQUAL
                    | NOTEQUAL
                    | LESS
                    | GREATER
                    | LEQUAL
                    | GEQUAL
<Variable>          : ID
                    | <Literal>
<Literal>           : INTEGER
                    | REAL
                    | STRING
                    | DATE
                    | TIME
"""

from pireal.interpreter.tokens import (
    TokenTypes,
    BINARY_OPERATORS,
)
from pireal.interpreter.exceptions import ConsumeError
from pireal.interpreter.exceptions import DuplicateRelationNameError

from pireal.interpreter.scanner import Scanner
from pireal.interpreter.lexer import Lexer
from pireal.interpreter import rast as ast


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
        return self.compound()

    def compound(self):
        nodes = []
        while self.token.type is not TokenTypes.EOF:
            nodes.append(self.query())

        compound = ast.Compound()
        compound.children = nodes

        return compound

    def query(self):
        node = self.assignment()
        self.consume(TokenTypes.SEMI)
        return node

    def assignment(self):
        variable = self.variable()
        self.consume(TokenTypes.ASSIGNMENT)
        expr = self.expression()

        node = ast.Assignment(variable, expr)

        return node

    def expression(self):
        if self.token.type is TokenTypes.PROJECT:
            node = self.project_expression()
        elif self.token.type is TokenTypes.SELECT:
            node = self.select_expression()
        elif self.token.type is TokenTypes.LPAREN:
            self.consume(TokenTypes.LPAREN)
            node = self.expression()
            self.consume(TokenTypes.RPAREN)
        elif self.token.type is TokenTypes.ID:
            node = self.variable()
            if self.token.value in BINARY_OPERATORS:
                # Binary expression
                # now, node is left node in binary expression
                token_type = BINARY_OPERATORS[self.token.value]
                self.consume(self.token.type)
                node = ast.BinaryOp(
                    left=node,
                    op=token_type,
                    right=self.expression()  # to allow (<Expression>)
                )

        return node

    def variable(self):
        node = ast.Variable(self.token)
        self.consume(TokenTypes.ID)
        return node

    def project_expression(self):
        self.consume(TokenTypes.PROJECT)
        attributes = self.attributes()
        self.consume(TokenTypes.LPAREN)
        expr = self.expression()
        self.consume(TokenTypes.RPAREN)

        node = ast.ProjectExpr(attributes, expr)
        return node

    def select_expression(self):
        self.consume(TokenTypes.SELECT)
        boolean_expr = self.boolean_expression()
        self.consume(TokenTypes.LPAREN)
        expr = self.expression()
        self.consume(TokenTypes.RPAREN)

        node = ast.SelectExpr(boolean_expr, expr)
        return node

    def boolean_expression(self):
        node = self.formula()

        while self.token.type is TokenTypes.AND or self.token.type is TokenTypes.OR:
            if self.token.type is TokenTypes.AND:
                boolean_operator = TokenTypes.AND
                self.consume(TokenTypes.AND)
            elif self.token.type is TokenTypes.OR:
                boolean_operator = TokenTypes.OR
                self.consume(TokenTypes.OR)

            boolean_node = ast.BooleanExpression(
                left_formula=node,
                operator=boolean_operator,
                right_formula=self.formula()
            )
            node = boolean_node

        return node

    def formula(self):
        left_operand = self.operand()
        operator = self.operator()
        right_operand = self.operand()

        node = ast.Condition(left_operand, operator, right_operand)

        return node

    def operand(self):
        if self.token.type is TokenTypes.ID:
            node = self.variable()
        else:
            node = self.literal()
        return node

    def literal(self):
        if self.token.type is TokenTypes.INTEGER:
            node = ast.Number(self.token)
            self.consume(TokenTypes.INTEGER)
        elif self.token.type is TokenTypes.REAL:
            node = ast.Number(self.token)
            self.consume(TokenTypes.REAL)
        elif self.token.type is TokenTypes.STRING:
            node = ast.String(self.token)
            self.consume(TokenTypes.STRING)
        elif self.token.type is TokenTypes.DATE:
            node = ast.Date(self.token)
            self.consume(TokenTypes.DATE)
        elif self.token.type is TokenTypes.TIME:
            node = ast.Time(self.token)
            self.consume(TokenTypes.TIME)

        return node

    def operator(self):
        node = self.token

        operators = [
            TokenTypes.EQUAL,
            TokenTypes.NOTEQUAL,
            TokenTypes.LESS,
            TokenTypes.LEQUAL,
            TokenTypes.GREATER,
            TokenTypes.GEQUAL,
        ]
        index = operators.index(node.type)
        op = operators[index]
        self.consume(op)
        return node

    def attributes(self):
        """Return a list of ast.Variable nodes"""
        node = self.variable()

        attribute_list = [node]
        while self.token.type is TokenTypes.COMMA:
            self.consume(TokenTypes.COMMA)
            attribute_list.append(self.variable())

        return attribute_list


class Interpreter(ast.NodeVisitor):
    """ Este objeto es el encargado de 'visitar' los nodos con el
    método Interpreter.to_python(), que convierte a un string que luego
    es evaluado como código Python

    `global_memory` es un diccionario ordenado que guarda las consultas 'reales'
    que serán evaluadas, hace de "symbol table".
    """

    def __init__(self, tree):
        self.tree = tree
        self.global_memory = {}

    def to_python(self):
        return self.visit(self.tree)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assignment(self, node):
        rname = self.visit(node.rname)
        if rname in self.global_memory:
            raise DuplicateRelationNameError(rname)
        self.global_memory[rname] = self.visit(node.query)

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
        bool_expr = self.visit(node.condition)
        expr = self.visit(node.expr)

        return f'{expr}.select("{bool_expr}")'

    def visit_BooleanExpression(self, node):
        left_formula = self.visit(node.left_formula)
        right_formula = self.visit(node.right_formula)

        return f'{left_formula} {node.operator.value} {right_formula}'

    def visit_Condition(self, node):
        left_operand = self.visit(node.op1)
        operator = node.operator.value
        right_operand = self.visit(node.op2)

        # Convert RA operator to valid Python operator
        map_operators = {
            '=': '==',
            '<>': '!='
        }
        operator = map_operators.get(operator, operator)

        return f'{left_operand} {operator} {right_operand}'

    def visit_Variable(self, node):
        return node.value

    def visit_Date(self, node):
        return repr(node.date)

    def visit_Time(self, node):
        return repr(node.time)

    def visit_String(self, node):
        return repr(node.string)

    def clear(self):
        self.global_memory.clear()


def interpret(query: str):
    return parse(query)


def parse(query: str) -> dict:
    scanner = Scanner(query)
    lexer = Lexer(scanner)
    try:
        parser = Parser(lexer)
        tree = parser.parse()
    except Exception as exc:
        print(exc)
        return {}
    else:
        interpreter = Interpreter(tree)
        interpreter.to_python()
        return interpreter.global_memory
