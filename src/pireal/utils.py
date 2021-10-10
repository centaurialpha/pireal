import logging

logger = logging.getLogger('pireal.utils')


def eval_expr(expr: str, names: dict):
    allowed_names = {}
    allowed_names.update(names)

    code = compile(expr, '<string>', 'eval')
    try:
        return eval(
            code,
            {'__builtins__': {}, 'datetime': __import__('datetime')},
            allowed_names
        )
    except Exception:
        logger.exception('Error during evaluate expression')
