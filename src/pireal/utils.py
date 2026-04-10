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

import logging

logger = logging.getLogger("pireal.utils")


class DatabaseSyntaxError(Exception):
    pass


def eval_expr(expr: str, names: dict):
    allowed_names = {}
    allowed_names.update(names)
    code = compile(expr, "<string>", "eval")
    try:
        return eval(
            code,
            {
                "__builtins__": {},
                "datetime": __import__("datetime"),
                "int": int,
                "float": float,
            },
            allowed_names,
        )
    except (TypeError, ValueError):
        return False
    except Exception:
        logger.exception("Error during evaluate expression")


def _eval_expr(expr: str, names: dict):
    allowed_names = {}
    allowed_names.update(names)

    code = compile(expr, "<string>", "eval")
    try:
        return eval(
            code,
            {"__builtins__": {}, "datetime": __import__("datetime")},
            allowed_names,
        )
    except Exception:
        logger.exception("Error during evaluate expression")


def sanitize_data(data: str):
    result = {"tables": []}

    lines = data.strip().splitlines()
    current_table: dict | None = None

    for line in lines:
        if not line:
            continue
        if line.startswith("@"):
            try:
                name, headers_str = line[1:].split(":", 1)
            except ValueError as err:
                raise DatabaseSyntaxError from err

            current_table = {
                "name": name.strip(),
                "header": [header.strip() for header in headers_str.split(",")],
                "tuples": [],
            }
            result["tables"].append(current_table)
        elif current_table:
            current_table["tuples"].append(tuple(value.strip() for value in line.split(",")))

    return result
