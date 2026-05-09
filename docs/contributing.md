# Contributing

Contributions are welcome. Whether it is a bug report, a new feature, or a documentation fix — everything helps.

---

## Setting up the development environment

Pireal uses [uv](https://docs.astral.sh/uv/) to manage dependencies.

```bash
git clone https://github.com/centaurialpha/pireal
cd pireal
uv sync --group dev
```

To run Pireal from source:

```bash
uv run pireal
```

---

## Running tests

```bash
uv run pytest
```

Interpreter tests only:

```bash
uv run pytest -m interpreter
```

GUI tests only:

```bash
uv run pytest -m gui
```

---

## Type checking

Pireal uses [ty](https://github.com/astral-sh/ty) as its type checker:

```bash
uvx ty check
```

---

## Linting and formatting

```bash
uv run ruff check src/
uv run ruff format src/
```

---

## Project structure

```
pireal/
├── src/pireal/
│   ├── core/             # Relation, DB, and central logic with no Qt dependencies
│   ├── interpreter/      # Lexer, Parser, Evaluator, AST
│   │   ├── lexer.py
│   │   ├── parser.py
│   │   ├── evaluator.py
│   │   └── rast.py       # AST nodes
│   ├── gui/              # PyQt6 interface
│   │   ├── services/     # DatabaseService, QueryService
│   │   ├── dialogs/      # Dialogs
│   │   └── theme/        # Themes and colors
│   ├── cli/              # Terminal mode (REPL)
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── gui/
├── docs/
└── pyproject.toml
```

!!! note "Important rule"
    `core/` and `interpreter/` are pure Python, no PyQt6 imports. Everything that depends on Qt goes in `gui/`.

---

## Making changes

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-feature`
3. Make your changes and add tests
4. Run the tests: `uv run pytest`
5. Open a Pull Request

---

## Reporting bugs

Open an issue on [GitHub](https://github.com/centaurialpha/pireal/issues) with:

- What you did
- What you expected to happen
- What actually happened
- Your operating system and Pireal version

---

## Building the documentation locally

```bash
uv sync --group docs
uv run mkdocs serve
```

Open [http://localhost:8000](http://localhost:8000). The documentation rebuilds automatically when you edit files.
