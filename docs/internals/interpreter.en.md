# The Interpreter

> *"If you don't know how compilers work, then you don't know how computers work. If you're not 100% sure whether you know how compilers work, then you don't know how they work."*
> — Steve Yegge

The core of Pireal is its Relational Algebra interpreter, built entirely from scratch in Python. It doesn't rely on any external parsing library — every component was designed and implemented by hand.

Understanding how an interpreter works is one of the most valuable topics in Software Engineering. Pireal is a real, small, and readable example of these concepts in action.

---

## Why build an interpreter from scratch?

Libraries like ANTLR, PLY, and Lark can generate parsers automatically. Using them would have been faster, but Pireal's goal isn't just to work — it's to be a **didactic example** of how a formal language gets processed.

Relational Algebra also has a relatively simple grammar that can be implemented with a recursive descent parser without too much complexity. This makes it ideal for understanding the concepts without drowning in edge cases.

---

## Pipeline architecture

A query like this:

```
q := project name (select age = 25 (students));
```

Goes through four stages before producing a result:

```
Source text
    │
    ▼
┌─────────┐
│ Scanner │  Wraps the text in a character-by-character navigation interface
└─────────┘
    │
    ▼
┌───────┐
│ Lexer │  Groups characters into meaningful tokens
└───────┘
    │
    ▼
┌────────┐
│ Parser │  Builds the AST (Abstract Syntax Tree)
└────────┘
    │
    ▼
┌───────────┐
│ Evaluator │  Traverses the AST and executes relational operations
└───────────┘
    │
    ▼
Relation (result)
```

---

## Scanner

The `Scanner` is the lowest layer. It receives the source text as a string and wraps it to expose a navigation interface: advancing character by character, peeking at the next one without consuming it, and tracking the current line number.

Its only responsibility is navigation over the text. It knows nothing about tokens or grammar.

---

## Lexer (tokenizer)

The `Lexer` uses the Scanner to group characters into **tokens** — the smallest meaningful units of the language.

For example, `select age = 25` produces:

| Token    | Type        |
|----------|-------------|
| `select` | `SELECT`    |
| `age`    | `ID`        |
| `=`      | `EQUAL`     |
| `25`     | `INTEGER`   |

---

## Parser

The `Parser` consumes tokens from the Lexer and builds an **AST (Abstract Syntax Tree)** — a tree representation of the logical structure of the query.

It implements a **recursive descent parser**: each grammar rule corresponds to a Python method.

For `q := project name (select age = 25 (students))`, the resulting AST is:

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

The `Evaluator` implements the **Visitor pattern** on the AST. It traverses the tree top-down and executes each node by calling the corresponding method.

```python
class Evaluator(NodeVisitor):
    def visit_ProjectExpr(self, node):
        relation = self.visit(node.expr)
        attrs = [attr.value for attr in node.attrs]
        return relation.project(*attrs)

    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return getattr(left, BINARY_OP_MAP[node.op])(right)
```

!!! note "Why Visitor?"
    The Visitor pattern lets you add new operations on the AST without modifying the nodes. For example, Pireal also has a `SQLGenerator` that traverses the same tree and produces equivalent SQL — without touching the evaluator or parser code.

---

## The Relation class

`Relation` is the data type that flows between all operators. Internally it stores:

- `header`: list of column names
- `content`: a set of tuples (Python set, guarantees uniqueness)

Each relational operation (`.project()`, `.select()`, `.njoin()`, etc.) returns a new `Relation` without modifying the original.

---

## Explore the code

- `src/pireal/interpreter/scanner.py`
- `src/pireal/interpreter/lexer.py`
- `src/pireal/interpreter/parser.py`
- `src/pireal/interpreter/rast.py` — AST node definitions
- `src/pireal/interpreter/evaluator.py`
- `src/pireal/core/relation.py`
