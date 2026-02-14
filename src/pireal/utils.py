import logging

logger = logging.getLogger("pireal.utils")


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
    current_table = None

    for line in lines:
        if not line:
            continue
        if line.startswith("@"):
            table_def = line[1:]
            name, headers_str = table_def.split(":")
            headers = headers_str.split(",")

            current_table = {
                "name": name,
                "header": headers,
                "tuples": [],
            }
            result["tables"].append(current_table)
        elif current_table:
            values = tuple(line.split(","))
            current_table["tuples"].append(values)

    return result
