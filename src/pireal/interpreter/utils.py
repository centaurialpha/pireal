# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from __future__ import annotations

import datetime
from difflib import get_close_matches

from pireal.interpreter import rast as ast
from pireal.interpreter.tokens import TokenTypes

_DATE_FORMATS = ("%d/%m/%Y", "%Y/%m/%d", "%Y-%m-%d")


def is_date(string) -> tuple[bool, datetime.date | None]:
    for fmt in _DATE_FORMATS:
        try:
            return True, datetime.datetime.strptime(string, fmt).date()
        except ValueError:
            continue
    return False, None


def is_time(string) -> tuple[bool, datetime.time | None]:
    ok = True
    time = None
    try:
        time = datetime.datetime.strptime(string, "%H:%M").time()
    except ValueError:
        ok = False
    return ok, time


def condition_to_string(condition) -> str:
    """Convierte AST de condición a string evaluable"""
    if isinstance(condition, ast.Condition):
        op1 = operand_to_string(condition.op1)
        op2 = operand_to_string(condition.op2)
        operator = condition.operator.value
        return f"{op1} {operator} {op2}"
    elif isinstance(condition, ast.BooleanExpression):
        left = condition_to_string(condition.left_formula)
        right = condition_to_string(condition.right_formula)
        op = "and" if condition.operator == TokenTypes.AND else "or"
        return f"({left}) {op} ({right})"
    return str(condition)


def operand_to_string(operand, *, for_display=False) -> str:
    """Convierte operando a string.

    Args:
        operand: Nodo AST del operando
        for_display: Si True, formato legible. Si False, formato evaluable.
    """
    if isinstance(operand, ast.Variable):
        return operand.value
    elif isinstance(operand, ast.Number):
        return str(operand.value)
    elif isinstance(operand, ast.String):
        return f"'{operand.value}'"
    elif isinstance(operand, ast.Date):
        date_val = operand.value
        if for_display:
            return f"'{date_val.strftime('%d/%m/%Y')}'"
        return f"datetime.date({date_val.year}, {date_val.month}, {date_val.day})"
    elif isinstance(operand, ast.Time):
        time_val = operand.value
        if for_display:
            return f"'{time_val.strftime('%H:%M')}'"
        return f"datetime.time({time_val.hour}, {time_val.minute})"
    return str(operand)


def suggest_closest(word: str, candidates: list[str]) -> str | None:
    matches = get_close_matches(word, candidates, n=1, cutoff=0.6)
    return matches[0] if matches else None
