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
"""BNF.

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

from pireal.interpreter import rast as ast
from pireal.interpreter.exceptions import ConsumeError
from pireal.interpreter.lexer import Lexer
from pireal.interpreter.scanner import Scanner
from pireal.interpreter.tokens import BINARY_OPERATORS, Token, TokenTypes


class Parser(object):
    """The Parser.

    Is the part that really understands the syntax of
    the language. It calls the Lexer to get tokens and processes the tokens
    per the syntax of the language.
    """

    def __init__(self, lexer):
        self.lexer = lexer
        self.token: Token = self.lexer.next_token()

    def consume(self, token_type):
        """Consume a token of a given type and get the next token.

        If the current token is not of the expected type, then
        raise an error
        """
        if self.token.type == token_type:
            self.token = self.lexer.next_token()
        else:
            raise ConsumeError(
                token_type,
                self.token.type,
                self.lexer.sc.lineno,
                got_value=str(self.token.value),
            )

    def parse(self):
        return self.compound()

    def compound(self) -> ast.Compound:
        children = []
        while self.token.type is not TokenTypes.EOF:
            children.append(self.query())
        return ast.Compound(children=children)

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
        elif self.token.type is TokenTypes.LEFT_PARENTHESIS:
            self.consume(TokenTypes.LEFT_PARENTHESIS)
            node = self.expression()
            self.consume(TokenTypes.RIGHT_PARENTHESIS)
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
                    right=self.expression(),  # to allow (<Expression>)
                )

        return node

    def variable(self):
        node = ast.Variable(self.token)
        self.consume(TokenTypes.ID)
        return node

    def project_expression(self):
        self.consume(TokenTypes.PROJECT)
        attributes = self.attributes()
        self.consume(TokenTypes.LEFT_PARENTHESIS)
        expr = self.expression()
        self.consume(TokenTypes.RIGHT_PARENTHESIS)

        node = ast.ProjectExpr(attributes, expr)
        return node

    def select_expression(self):
        self.consume(TokenTypes.SELECT)
        boolean_expr = self.boolean_expression()
        self.consume(TokenTypes.LEFT_PARENTHESIS)
        expr = self.expression()
        self.consume(TokenTypes.RIGHT_PARENTHESIS)

        node = ast.SelectExpr(boolean_expr, expr)
        return node

    def boolean_expression(self) -> ast.BooleanExpression | ast.Condition:
        node = self.formula()

        while self.token.type in (TokenTypes.AND, TokenTypes.OR):
            operator = self.token.type
            self.consume(operator)
            node = ast.BooleanExpression(
                left_formula=node,
                operator=operator,
                right_formula=self.formula(),
            )

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
        token_type = self.token.type
        value = self.token.value

        litarl_map = {
            TokenTypes.INTEGER: ast.Number,
            TokenTypes.REAL: ast.Number,
            TokenTypes.STRING: ast.String,
            TokenTypes.DATE: ast.Date,
            TokenTypes.TIME: ast.Time,
        }

        node_class = litarl_map.get(token_type)
        if node_class is None:
            raise ConsumeError(TokenTypes.INTEGER, token_type, self.lexer.sc.lineno)

        self.consume(token_type)
        return node_class(value)

    def operator(self) -> Token:
        COMPARISON_OPERATORS = {
            TokenTypes.EQUAL,
            TokenTypes.NOTEQUAL,
            TokenTypes.LESS,
            TokenTypes.LESS_EQUAL,
            TokenTypes.GREATER,
            TokenTypes.GREATER_EQUAL,
        }

        if self.token.type not in COMPARISON_OPERATORS:
            raise ConsumeError(TokenTypes.EQUAL, self.token.type, self.lexer.sc.lineno)

        token = self.token
        self.consume(self.token.type)
        return token

    def attributes(self):
        """Return a list of ast.Variable nodes."""
        node = self.variable()

        attribute_list = [node]
        while self.token.type is TokenTypes.COMMA:
            self.consume(TokenTypes.COMMA)
            attribute_list.append(self.variable())

        return attribute_list


def parse(query: str) -> ast.Compound:
    return Parser(Lexer(Scanner(query))).parse()
