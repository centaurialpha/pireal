import pytest
from pireal.interpreter.lexer import Lexer
from pireal.interpreter.parser import Parser
from pireal.interpreter.scanner import Scanner
from pireal.interpreter.tree_builder import NodeKind, TreeBuilder, TreeNode

pytestmark = pytest.mark.interpreter


def build(query: str) -> list[TreeNode]:
    tree = Parser(Lexer(Scanner(query))).parse()
    return TreeBuilder().build(tree)


@pytest.mark.parametrize(
    "query, expected_label, expected_kind",
    [
        ("q := personas;", "personas", NodeKind.RELATION),
        ("q := select age=25 (personas);", "σ (age = 25)", NodeKind.UNARY_OP),
        ("q := project name, age (personas);", "π name, age", NodeKind.UNARY_OP),
        ("q := personas njoin salarios;", "⋈", NodeKind.BINARY_OP),
        ("q := personas union salarios;", "∪", NodeKind.BINARY_OP),
        ("q := personas intersect salarios;", "∩", NodeKind.BINARY_OP),
        ("q := personas difference salarios;", "−", NodeKind.BINARY_OP),
        ("q := personas product salarios;", "×", NodeKind.BINARY_OP),
        ("q := personas louter salarios;", "⟕", NodeKind.BINARY_OP),
        ("q := personas router salarios;", "⟖", NodeKind.BINARY_OP),
        ("q := personas fouter salarios;", "⟗", NodeKind.BINARY_OP),
    ],
)
def test_root_node(query, expected_label, expected_kind):
    roots = build(query)
    assert len(roots) == 1
    assert roots[0].label == "q"
    assert roots[0].kind == NodeKind.ASSIGNMENT
    child = roots[0].children[0]
    assert child.label == expected_label
    assert child.kind == expected_kind


def test_assignment_has_relation_child():
    roots = build("q := personas;")
    child = roots[0].children[0]
    assert child.label == "personas"
    assert child.kind == NodeKind.RELATION
    assert child.children == []


def test_select_condition_label():
    roots = build("q := select age>=18 (personas);")
    sigma = roots[0].children[0]
    assert "age" in sigma.label
    assert "≥" in sigma.label
    assert "18" in sigma.label


def test_project_attrs():
    roots = build("q := project name, age, id (personas);")
    pi = roots[0].children[0]
    assert "name" in pi.label
    assert "age" in pi.label
    assert "id" in pi.label


def test_binary_op_children():
    roots = build("q := r1 njoin r2;")
    join = roots[0].children[0]
    assert len(join.children) == 2
    assert join.children[0].label == "r1"
    assert join.children[1].label == "r2"


def test_nested_select_project():
    roots = build("q := select age=25 (project name, age (personas));")
    sigma = roots[0].children[0]
    assert sigma.kind == NodeKind.UNARY_OP
    pi = sigma.children[0]
    assert pi.kind == NodeKind.UNARY_OP
    assert pi.children[0].label == "personas"


def test_multiple_assignments():
    roots = build("q1 := personas; q2 := salarios;")
    assert len(roots) == 2
    assert roots[0].label == "q1"
    assert roots[1].label == "q2"


def test_boolean_and_condition():
    roots = build("q := select age>=18 and age<=30 (personas);")
    sigma = roots[0].children[0]
    assert "∧" in sigma.label


def test_boolean_or_condition():
    roots = build("q := select age=18 or age=30 (personas);")
    sigma = roots[0].children[0]
    assert "∨" in sigma.label
