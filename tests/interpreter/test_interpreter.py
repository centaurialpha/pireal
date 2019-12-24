import pytest


from pireal.core.interpreter import lexer
from pireal.core.interpreter import parser
from pireal.core.interpreter import rast as ast


# def test_visit_Assignment():
#     tkn = lexer.Token(lexer.ID, 'q1')
#     node_variable = ast.Variable(tkn)

#     node_attr1 = ast.Variable(lexer.Token(lexer.ID, 'a'))
#     node_attr2 = ast.Variable(lexer.Token(lexer.ID, 'b'))

#     node_rela = ast.Variable(lexer.Token(lexer.ID, 'p'))
#     node_query = ast.ProjectExpr(
#         [node_attr1, node_attr2],
#         node_rela
#     )
#     node_ass = ast.Assignment(node_variable, node_query)

#     inter = parser.Interpreter(None)
#     inter.visit_Assignment(node_ass)
#     assert inter.SCOPE['q1'] == "p.project('a', 'b')"


# def test_visit_Num():
#     tkn = lexer.Token(lexer.INTEGER, 23)
#     node_number = ast.Number(tkn)
#     inter = parser.Interpreter(None)
#     assert inter.visit_Number(node_number) == 23


# def test_visit_Variable():
#     node_var = ast.Variable(lexer.Token(lexer.ID, 'persona'))
#     inter = parser.Interpreter(None)
#     expected = 'persona'
#     assert inter.visit_Variable(node_var) == expected


# def test_visit_Select():
#     var = ast.Variable(lexer.Token(lexer.ID, 'edad'))
#     var2 = ast.Number(lexer.Token(lexer.INTEGER, 11))
#     operator = lexer.Token(lexer.GREATER, '>')
#     node_condition = ast.Condition(var, operator, var2)
#     node_rela = ast.Variable(lexer.Token(lexer.ID, 'p'))

#     node_select = ast.SelectExpr(node_condition, node_rela)
#     # print(node_select.operator)
#     inter = parser.Interpreter(None)
#     expected = "p.select(\"edad > 11\")"
#     assert inter.visit_SelectExpr(node_select) == expected


# def test_visit_Project():
#     node_attr1 = ast.Variable(lexer.Token(lexer.ID, 'a'))
#     node_attr2 = ast.Variable(lexer.Token(lexer.ID, 'b'))

#     node_rela = ast.Variable(lexer.Token(lexer.ID, 'p'))

#     node_projection = ast.ProjectExpr(
#         [node_attr1, node_attr2],
#         node_rela
#     )
#     expected = "p.project('a', 'b')"
#     inter = parser.Interpreter(None)
#     assert inter.visit_ProjectExpr(node_projection) == expected


