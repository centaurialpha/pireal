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

import pytest

from pireal.interpreter.lexer import Lexer
from pireal.interpreter.parser import Parser
from pireal.interpreter.query_plan import (
    NodeState,
    OperatorType,
    QueryPlanBuilder,
    QueryPlanEvaluator,
)
from pireal.interpreter.scanner import Scanner
from tests.helpers import make_relation


@pytest.fixture
def sample_relations():
    estudiantes = make_relation(
        ["id", "nombre", "edad"], [("1", "Gabriel", "25"), ("2", "Marisel", "22"), ("3", "Rodrigo", "30")]
    )
    estudiantes.name = "estudiantes"

    materias = make_relation(["id", "nombre"], [("1", "BD"), ("2", "Algo")])
    materias.name = "materias"

    return {"estudiantes": estudiantes, "materias": materias}


def test_build_simple_select(sample_relations):
    """Test construcción de árbol con select simple"""
    query = "q := select edad > 25 (estudiantes);"
    tree = Parser(Lexer(Scanner(query))).parse()
    builder = QueryPlanBuilder(sample_relations)
    plans = builder.build(tree)

    assert len(plans) == 1
    plan = plans[0]

    # Raíz es select
    assert plan.operator == OperatorType.SELECT
    assert "edad" in plan.params
    assert len(plan.children) == 1

    # Hijo es relación base
    child = plan.children[0]
    assert child.operator == OperatorType.RELATION
    assert child.params == "estudiantes"
    assert child.is_leaf()


def test_build_nested_operations(sample_relations):
    """Test construcción de árbol con operaciones anidadas"""
    query = "q := project nombre (select edad >= 25 (estudiantes));"
    tree = Parser(Lexer(Scanner(query))).parse()
    builder = QueryPlanBuilder(sample_relations)
    plans = builder.build(tree)

    plan = plans[0]

    # Raíz: project
    assert plan.operator == OperatorType.PROJECT
    assert "nombre" in plan.params

    # Hijo: select
    child = plan.children[0]
    assert child.operator == OperatorType.SELECT
    assert "edad" in child.params

    # Nieto: relación
    grandchild = child.children[0]
    assert grandchild.operator == OperatorType.RELATION
    assert grandchild.params == "estudiantes"


def test_build_binary_operation(sample_relations):
    """Test construcción de árbol con operador binario"""
    query = "q := estudiantes njoin materias;"
    tree = Parser(Lexer(Scanner(query))).parse()
    builder = QueryPlanBuilder(sample_relations)
    plans = builder.build(tree)

    plan = plans[0]

    # Raíz: njoin
    assert plan.operator == OperatorType.NJOIN
    assert len(plan.children) == 2

    # Hijos son relaciones
    assert plan.children[0].operator == OperatorType.RELATION
    assert plan.children[1].operator == OperatorType.RELATION


def test_expand_intermediate_queries(sample_relations):
    """Test expansión de queries intermedias"""
    query = """
    mayores := select edad >= 25 (estudiantes);
    resultado := project nombre (mayores);
    """
    tree = Parser(Lexer(Scanner(query))).parse()
    builder = QueryPlanBuilder(sample_relations)
    plans = builder.build(tree)

    # Segundo plan (resultado) debe tener el select expandido
    plan = plans[1]

    # Raíz: project
    assert plan.operator == OperatorType.PROJECT

    # Hijo debe ser select (expandido), no Variable
    child = plan.children[0]
    assert child.operator == OperatorType.SELECT
    assert child.operator != OperatorType.RELATION

    # Nieto: relación base
    grandchild = child.children[0]
    assert grandchild.operator == OperatorType.RELATION
    assert grandchild.params == "estudiantes"


def test_evaluator_leaf_node(sample_relations):
    """Test evaluación de nodo hoja"""
    query = "q := estudiantes;"
    tree = Parser(Lexer(Scanner(query))).parse()
    builder = QueryPlanBuilder(sample_relations)
    plans = builder.build(tree)

    evaluator = QueryPlanEvaluator(sample_relations)
    result = evaluator.evaluate(plans[0])

    assert result.cardinality() == 3
    assert result.degree() == 3
    assert plans[0].state == NodeState.EXECUTED


def test_evaluator_select(sample_relations):
    """Test evaluación de select"""
    query = "q := select edad >= 25 (estudiantes);"
    tree = Parser(Lexer(Scanner(query))).parse()
    builder = QueryPlanBuilder(sample_relations)
    plans = builder.build(tree)

    evaluator = QueryPlanEvaluator(sample_relations)
    result = evaluator.evaluate(plans[0])

    assert result.cardinality() == 2  # Gabriel(25) y Rodrigo(30)
    assert result.degree() == 3
    assert plans[0].state == NodeState.EXECUTED


def test_evaluator_project(sample_relations):
    """Test evaluación de project"""
    query = "q := project nombre (estudiantes);"
    tree = Parser(Lexer(Scanner(query))).parse()
    builder = QueryPlanBuilder(sample_relations)
    plans = builder.build(tree)

    evaluator = QueryPlanEvaluator(sample_relations)
    result = evaluator.evaluate(plans[0])

    assert result.cardinality() == 3
    assert result.degree() == 1
    assert "nombre" in result.header


def test_evaluator_caching(sample_relations):
    """Test que el evaluador cachea resultados"""
    query = "q := select edad > 25 (estudiantes);"
    tree = Parser(Lexer(Scanner(query))).parse()
    builder = QueryPlanBuilder(sample_relations)
    plans = builder.build(tree)

    evaluator = QueryPlanEvaluator(sample_relations)

    # Primera evaluación
    result1 = evaluator.evaluate(plans[0])

    # Segunda evaluación (debe usar cache)
    result2 = evaluator.evaluate(plans[0])

    assert result1 is result2  # mismo objeto


def test_evaluator_error_handling(sample_relations):
    """Test manejo de errores en evaluación"""
    query = "q := select nonexistent = 1 (estudiantes);"
    tree = Parser(Lexer(Scanner(query))).parse()
    builder = QueryPlanBuilder(sample_relations)
    plans = builder.build(tree)

    evaluator = QueryPlanEvaluator(sample_relations)

    with pytest.raises(SyntaxError):
        evaluator.evaluate(plans[0])

    assert plans[0].state == NodeState.ERROR
