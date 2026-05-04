# The interpreter

> *"If you don't know how compilers work, then you don't know how computers work. If you're not 100% sure how compilers work, then you don't know how computers work."*
> -- Steve Yegge

The core of Pireal is its Relational Algebra interpreter, built entirely from scratch in Python. It does not depend on any external parsing library -- every component was designed and implemented by hand.

Understanding how an interpreter works is one of the most valuable topics in a Software Engineering degree. Pireal is a real, small, and readable example of these concepts in action.

---

## Why build an interpreter from scratch?

There are libraries that generate parsers automatically (ANTLR, PLY, Lark). Using them would have been faster, but Pireal's goal is not just to work -- it is to be a **didactic example** of how a formal language is processed.

Besides, Relational Algebra has a relatively simple grammar that can be implemented with a recursive descent parser without too much complexity. This makes it ideal for understanding the concepts without drowning in edge cases.

---

## Pipeline architecture

A query like this:

```
q := project name (select age = 25 (students));
```

Goes through four stages before producing a result:

```
Source text
    |
    v
┌─────────┐
│ Scanner │  Wraps the text to expose character-level navigation
└─────────┘
    |
    v
┌───────┐
│ Lexer │  Groups characters into meaningful tokens
└───────┘
    |
    v
┌────────┐
│ Parser │  Builds the AST (abstract syntax tree)
└────────┘
    |
    v
┌───────────┐
│ Evaluator │  Walks the AST and executes the relational operations
└───────────┘
    |
    v
Relation (result)
```

---

## Scanner

The `Scanner` is the lowest layer. It receives the source text as a string and wraps it to expose a navigation interface: advance character by character, peek at the next one without consuming it, and track the current line number.

```python
scanner = Scanner("select age = 25 (students)")
scanner.current_char   # 's'
scanner.advance()
scanner.current_char   # 'e'
scanner.lineno         # 1
```

Its only responsibility is navigating over the text. It knows nothing about tokens or grammar.

---

## Lexer (tokenizer)

The `Lexer` uses the Scanner to group characters into **tokens** -- the smallest meaningful units of the language.

For example, the text `select age = 25` produces:

| Token    | Type        |
|----------|-------------|
| `select` | `SELECT`    |
| `age`    | `ID`        |
| `=`      | `EQUAL`     |
| `25`     | `INTEGER`   |

The Lexer recognizes keywords (`select`, `project`, `njoin`, etc.), identifiers, numbers, single-quoted strings, dates, operators and punctuation symbols.

```python
lexer = Lexer(Scanner("select age = 25"))
lexer.next_token()  # Token(SELECT, 'select')
lexer.next_token()  # Token(ID, 'age')
lexer.next_token()  # Token(EQUAL, '=')
lexer.next_token()  # Token(INTEGER, '25')
```

---

## Parser

The `Parser` is the heart of the interpreter. It consumes tokens from the Lexer and builds an **AST (Abstract Syntax Tree)** -- a tree representation of the logical structure of the query.

It implements a **recursive descent parser**: each grammar rule corresponds to a Python method.

The (simplified) grammar of Pireal is:

```
program       ::= assignment+
assignment    ::= ID ':=' expression ';'
expression    ::= binary_expr | projection | selection | variable
projection    ::= 'project' attributes '(' expression ')'
selection     ::= 'select' condition '(' expression ')'
binary_expr   ::= expression operator expression
condition     ::= operand comparator operand
operator      ::= 'union' | 'intersect' | 'difference' | 'njoin' | ...
```

For the query `q := project name (select age = 25 (students))`, the resulting AST is:

```
Compound
└── Assignment(name='q')
    └── ProjectExpr(attrs=['name'])
        └── SelectExpr
            ├── Condition(op1='age', op='=', op2='25')
            └── Variable('students')
```

---

## Evaluator

The `Evaluator` implements the **Visitor** pattern over the AST. It walks the tree top-down and executes each node by calling the corresponding method.

```python
class Evaluator(NodeVisitor):
    def visit_Assignment(self, node):
        relation = self.visit(node.query)
        self._results[node.rname.value] = relation

    def visit_ProjectExpr(self, node):
        relation = self.visit(node.expr)
        attrs = [attr.value for attr in node.attrs]
        return relation.project(*attrs)

    def visit_SelectExpr(self, node):
        relation = self.visit(node.expr)
        condition = self.visit(node.condition)
        return relation.select(condition)

    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return getattr(left, BINARY_OP_MAP[node.op])(right)
```

The result of each `visit_*` is a `Relation`. At the end of evaluation, `_results` contains all the named relations shown to the user.

!!! note "Why Visitor?"
    The Visitor pattern lets you add new operations over the AST without modifying the nodes. For example, Pireal also has a `SQLGenerator` that walks the same tree and generates equivalent SQL -- without touching the evaluator or parser code.

---

## The Relation class

`Relation` is the data type that flows between all operators. Internally it stores:

- `header`: list of column names
- `content`: set of tuples (Python set, guarantees uniqueness)

```python
r = Relation()
r.header = ["id", "name", "age"]
r.insert(("1", "Gabriel", "25"))
r.insert(("2", "Marisel", "30"))

r.degree()       # 3  (number of columns)
r.cardinality()  # 2  (number of rows)
```

Each relational operation (`.project()`, `.select()`, `.njoin()`, etc.) returns a new `Relation` without modifying the original.

---

## Going deeper

If you want to explore the code:

- `src/pireal/interpreter/scanner.py` -- text navigation
- `src/pireal/interpreter/lexer.py` -- tokenization
- `src/pireal/interpreter/parser.py` -- AST construction
- `src/pireal/interpreter/rast.py` -- AST node definitions
- `src/pireal/interpreter/evaluator.py` -- execution
- `src/pireal/core/relation.py` -- the central data type

The integration tests in `tests/integration/` show the full pipeline end to end.
