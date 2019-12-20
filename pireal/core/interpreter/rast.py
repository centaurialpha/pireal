import datetime


class ParserError(Exception):
    pass


class DateFormatError(ParserError):
    pass


def parse_date(date: str):
    try:
        date_ = datetime.datetime.strptime(date, "%d/%m/%Y").date()
    except ValueError:
        try:
            date_ = datetime.datetime.strptime(date, "%Y/%m/%d").date()
        except ValueError:
            raise DateFormatError
    return date_


class AST(object):
    """ Base class for all nodes """
    pass


class Variable(AST):

    def __init__(self, token):
        self.token = token
        self.value = token.value


class Number(AST):

    def __init__(self, token):
        self.num = token.value
        self.token = token


class String(AST):

    def __init__(self, token):
        self.string = token.value
        self.token = token


class Date(AST):

    def __init__(self, token):

        self.date = parse_date(token.value)


class Time(AST):

    def __init__(self, token):
        hour, minute = map(int, token.value.split(':'))
        self.time = datetime.time(hour, minute)


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


class Condition(AST):

    def __init__(self, op1, operator, op2):
        self.op1 = op1
        self.operator = operator
        self.op2 = op2


class BoolOp(AST):

    def __init__(self):
        self.ops = []
        self.conditions = []


class Assignment(AST):

    def __init__(self, rname, query):
        self.rname = rname
        self.query = query


class Compound(AST):

    def __init__(self):
        self.children = []


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

        raise Exception(f'No visit_{node.__class__.__name__} method')
