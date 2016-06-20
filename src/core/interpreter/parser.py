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

# This module is responsible for organizing called "tokens" pieces,
# each of these tokens has a meaning in language

from src.core.interpreter.tokens import (
    SEMI,
    SEMICOLON,
    ID,
    CONSTANT,
    NUMBER,
    ASSIGNMENT,
    LPAREN,
    RPAREN,
    SEMI,
    SELECT,
    PROJECT,
    LESS,
    GREATER,
    LEQUAL,
    GEQUAL,
    EQUAL,
    NOTEQUAL,
    KEYWORDS
)


class AST(object):
    """ Base class for all nodes """
    pass


class AssignmentExpr(AST):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class Variable(AST):

    def __init__(self, token):
        self.token = token
        self.value = token.value


class ProjectExpr(AST):

    def __init__(self, attrs, expr):
        self.attrs = attrs
        self.expr = expr


class SelectExpr(AST):

    def __init__(self, cond, expr):
        self.condition = cond
        self.expr = expr


class BinaryOp(AST):

    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Formula(AST):

    def __init__(self, op1, operator, op2):
        self.op1 = op1
        self.operator = operator
        self.op2 = op2


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
            raise Exception("It is expected to find '{0}', "
                            "but '{1}' found, Line: {2}, Col:{3}".format(
                                token_type,
                                self.token.type,
                                self.lexer.sc.lineno,
                                self.lexer.sc.colno
                            ))

    def parse(self):
        """
        QueryDef : Query;
                 | AssignmentStatement;
        AssignmentStatement : RELATION_NAME := Query
        Query : Expression
        Expression : (Expression)
                   | SelectExpression
                   | ProjectExpression
                   | BinaryExpression
        SelectExpression : SELECT Condition (Expression)
        ProjectExpression : PROJECT Attributes (Expression)
        BinaryExpression : (Expression) BinaryOperator (Expression)
        Condition : AndCondition
                  | AndCondition OR Condition
        AndCondition : RelationFormula
                     | RelationFormula AND AndCondition
        RelationFormula : Operand RelationOperator Operand
                        | (Operand)
        BinaryOperator : UNION
                       | INTERSECT
                       | DIFFERENCE
                       | PRODUCT
                       | NJOIN
        Attributes : ID
                   | ID, Attributes
        Operand : ID
                | CONSTANT
        RelationOperator : =
                         | <>
                         | <
                         | >
                         | <=
                         | >=
        """

        tree = self._query_definition()
        self.consume(SEMICOLON)
        return tree

    def _query_definition(self):
        """
        QueryDef : Query;
                 | AssignmentStatement;
        """

        peek_token = self.lexer.peek()
        if self.token.type == ID and peek_token.type == ASSIGNMENT:
            node = self._assignment_statement()
        else:
            node = self._query()

        return node

    def _assignment_statement(self):
        """
        AssignmentStatement : RELATION_NAME := Query
        """
        relation_name = Variable(self.token)
        self.consume(ID)
        self.consume(ASSIGNMENT)
        query = self._query()
        node = AssignmentExpr(relation_name, query)
        return node

    def _query(self):
        """
        Query : Expression
        """
        node = self._expression()
        return node

    def _expression(self):
        """
        Expression : ID
                   | (Expression)
                   | SelectExpression
                   | ProjectExpression
                   | BinaryExpression
        """

        if self.token.type == ID:
            tkn_peek = self.lexer.peek().type
            if tkn_peek.lower() in KEYWORDS:
                node = self._binary_expression()
            else:
                node = Variable(self.token)
                self.consume(ID)
        elif self.token.type == LPAREN:
            self.consume(LPAREN)
            node = self._expression()
            self.consume(RPAREN)
        elif self.token.type == SELECT:
            node = self._select_expression()
        elif self.token.type == PROJECT:
            node = self._project_expression()

        return node

    def _binary_expression(self):
        """
        BinaryExpression : Expression BinaryOp Expression
        """

        node_left = self._expression()
        operator = self._binary_operator()
        node_right = self._expression()
        root = BinaryOp(node_left, operator, node_right)
        return root

    def _binary_operator(self):
        """
        BinaryOperator : UNION
                       | DIFFERENCE
                       | INTERSECT
                       | PRODUCT
                       | NJOIN
        """

        tkn_value = self.token.value
        tkn_type = KEYWORDS.get(tkn_value)
        self.consume(tkn_type)
        return tkn_type

    def _select_expression(self):
        """
        SelectExpression : SELECT Condition (Expression)
        """

        self.consume('SELECT')
        condition = self._condition()
        self.consume(LPAREN)
        expr = self._expression()
        self.consume(RPAREN)
        node = SelectExpr(condition, expr)
        return node

    def _condition(self):
        """
        Condition : AndCondition
                  | AndCondition OR Condition
        """
        # FIXME: OR
        and_condition = self._and_condition()
        return and_condition

    def _and_condition(self):
        """
        AndCondition : RelationFormula
                     | RelationFormula AND AndCondition
        """

        rformula = self._relation_formula()
        return rformula

    def _relation_formula(self):
        """
        RelationFormula : Operand RelationOperator Operand
                        | (Operand)
        """

        op1 = Variable(self.token)
        self.consume(ID)
        operator = self._operator()
        op2 = Variable(self.token)
        # FIXME: consume NUMBER and STRING, DATE
        # CONSTANT ?
        self.consume(NUMBER)
        formula = Formula(op1, operator, op2)
        return formula

    def _operator(self):
        """
        RelationOperator : =
                         | <>
                         | <
                         | >
                         | <=
                         | >=
        """

        tkn = self.token
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

        return tkn

    def _project_expression(self):
        """
        ProjectExpression : PROJECT Attributes (Expr)
        """

        self.consume('PROJECT')
        attributes = self._attributes()
        self.consume(LPAREN)
        expr = self._expression()
        self.consume(RPAREN)
        node = ProjectExpr(attributes, expr)
        return node

    def _attributes(self):
        """
        Attributes : ID
                   | ID, Attributes
        """

        node = Variable(self.token)
        self.consume(ID)

        results = [node]
        append = results.append

        while self.token.type == SEMI:
            self.consume(SEMI)
            append(Variable(self.token))
            self.consume(ID)

        return results


class NodeVisitor(object):
    """ Visitor pattern

    A node visitor base class that walks the abstract syntax tree and calls
    a visitor function for every node found. This function may return a value
    which is forwarded by the `visit` method.

    This class is meant to be subclassed, with the subclass adding visitor
    methods.

    Per default the visitor functions for the nodes are `visit_` + class
    name of the node. So a `BinOp` node visit function would be
    `visit_BinOp`. This behavior can be changed by overriding the `visit`
    method. If no visitor function exists for a node the `_generic_visit`
    visitor is used instead.
    """

    def visit(self, node):
        """ Visit a node """

        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node):
        """ Called if not explicit visitor function exists for a node """

        raise Exception("No visit_{} method".format(node.__class__.__name__))


class Interpreter(NodeVisitor):

    def __init__(self, parser):
        self.parser = parser
        self._q = ""

    def to_python(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def visit_AssignmentExpr(self, node):
        return self.visit(node.right)

    def visit_ProjectExpr(self, node):
        attrs = [self.visit(i) for i in node.attrs]
        proj_expr = "{0}.project({1})".format(
            self.visit(node.expr),
            ', '.join("'{0}'".format(i) for i in attrs)
        )
        return proj_expr

    def visit_Variable(self, node):
        return node.value

    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        expr = '{0}.{1}({2})'.format(
            left,
            node.op.value,
            right
        )
        return expr
