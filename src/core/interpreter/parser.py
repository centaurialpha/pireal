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

from src.core.interpreter.token import (
    SEMI,
    IDENTIFIER,
    ASSIGNMENT,
    LPAREN,
    RPAREN,
    COMA
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
                            "but '{1}' found".format(
                                token_type, self.token.type))

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
        SelectExpression : SELECT Condition (Expr)
        ProjectExpression : PROJECT Attributes (Expr)
        BinaryExpression : (Expr) BinaryOperator (Expr)
        Expr : ID
             | Expression
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
        self.consume(SEMI)
        return tree

    def _query_definition(self):
        """
        QueryDef : Query;
                 | AssignmentStatement;
        """

        if self.token.type == IDENTIFIER:
            node = self._assignment_statement()
        else:
            node = self._query()

        return node

    def _assignment_statement(self):
        """
        AssignmentStatement : RELATION_NAME := Query
        """
        relation_name = Variable(self.token)
        self.consume(IDENTIFIER)
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
        Expression : (Expression)
                   | SelectExpression
                   | ProjectExpression
                   | BinaryExpression
        """

        if self.token.type == LPAREN:
            self.consume(LPAREN)
            node = self._expression()
            self.consume(RPAREN)
        elif self.token.value == 'select':
            node = self._select_expression()
        elif self.token.value == 'project':
            node = self._project_expression()
        return node

    def _select_expression(self):
        """
        SelectExpression : SELECT Condition (Expr)
        """
        pass

    def _project_expression(self):
        """
        ProjectExpression : PROJECT Attributes (Expr)
        """

        self.consume('KEYWORD')
        attributes = self._attributes()
        self.consume(LPAREN)
        expr = self._expr()
        self.consume(RPAREN)
        node = ProjectExpr(attributes, expr)
        return node

    def _expr(self):
        """
        Expr : ID
             | Expression
        """

        if self.token.type == IDENTIFIER:
            node = Variable(self.token)
            self.consume(IDENTIFIER)
        else:
            node = self._expression()

        return node

    def _attributes(self):
        """
        Attributes : ID
                   | ID, Attributes
        """

        node = Variable(self.token)
        self.consume(IDENTIFIER)

        results = [node]
        append = results.append

        while self.token.type == COMA:
            self.consume(COMA)
            append(Variable(self.token))
            self.consume(IDENTIFIER)

        return results
