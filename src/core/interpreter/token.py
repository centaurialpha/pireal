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

IDENTIFIER = 'IDENTIFIER'
ASSIGNMENT = 'ASSIGNMENT'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
COMA = 'COMA'
SEMI = 'SEMI'
NUMBER = 'NUMBER'
STRING = 'STRING'
DATE = 'DATE'
EQUAL = 'EQUAL'
NEQUAL = 'NEQUAL'
GREATER = 'GREATER'
GREATEREQUAL = 'GREATEREQUAL'
LESS = 'LESS'
LESSEQUAL = 'LESSEQUAL'
EOF = 'EOF'


class Token(object):
    """ A Token is the kind of thing that Lexer returns.
    It holds:
    - The value of the token
    - The type of token that it is
    """

    __slots__ = ('type', 'value')

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """ Returns a representation of token. For example:

        Token(SEMI, ';')
        Token(IDENTIFIER, foo)
        Token(KEYWORD, select)
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=self.value
        )

    def __repr__(self):
        return self.__str__()


KEYWORDS = {
    'select': Token('KEYWORD', 'select'),
    'project': Token('KEYWORD', 'project'),
    'njoin': Token('KEYWORD', 'njoin'),
    'product': Token('KEYWORD', 'product'),
    'union': Token('KEYWORD', 'union'),
    'intersect': Token('KEYWORD', 'intersect'),
    'difference': Token('KEYWORD', 'difference'),
    'and': Token('KEYWORD', 'and'),
    'or': Token('KEYWORD', 'or')
}
