# Contributing

Contributions are welcome and appreciated. Whether it's a bug report, a new feature, or a documentation fix — everything helps.

---

## Development setup

Pireal uses [uv](https://docs.astral.sh/uv/) for dependency management.

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

Run only interpreter tests:

```bash
uv run pytest -m interpreter
```

---

## Project structure

```
pireal/
├── src/pireal/
│   ├── core/          # Relation model and core logic
│   ├── interpreter/   # Scanner, Lexer, Parser, Evaluator
│   │   ├── scanner.py
│   │   ├── lexer.py
│   │   ├── parser.py
│   │   ├── evaluator.py
│   │   └── rast.py    # AST node definitions
│   ├── gui/           # PyQt6 interface
│   └── main.py
├── tests/
│   ├── unit/
│   └── integration/
├── docs/              # This documentation
└── pyproject.toml
```

---

## Making changes

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-feature`
3. Make your changes and add tests
4. Run the test suite: `uv run pytest`
5. Open a Pull Request

---

## Reporting bugs

Open an issue on [GitHub](https://github.com/centaurialpha/pireal/issues) with:

- What you did
- What you expected to happen
- What actually happened
- Your OS and Python version

---

## Building the documentation locally

```bash
uv run mkdocs serve
```

Then open [http://localhost:8000](http://localhost:8000) in your browser. The docs rebuild automatically when you edit files.
