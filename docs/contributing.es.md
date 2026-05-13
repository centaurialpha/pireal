# Contribuir

Las contribuciones son bienvenidas. Ya sea un reporte de bug, una funcionalidad nueva, o una corrección en la documentación - todo ayuda.

---

## Configurar el entorno de desarrollo

Pireal usa [uv](https://docs.astral.sh/uv/) para gestionar dependencias.

```bash
git clone https://github.com/centaurialpha/pireal
cd pireal
uv sync --group dev
```

Para ejecutar Pireal desde el código fuente:

```bash
uv run pireal
```

---

## Ejecutar los tests

```bash
uv run pytest
```

Solo los tests del intérprete:

```bash
uv run pytest -m interpreter
```

Solo los tests de la GUI:

```bash
uv run pytest -m gui
```

---

## Type checking

Pireal usa [ty](https://github.com/astral-sh/ty) como type checker:

```bash
uvx ty check
```

---

## Linting y formato

```bash
uv run ruff check src/
uv run ruff format src/
```

---

## Estructura del proyecto

```
pireal/
├── src/pireal/
│   ├── core/             # Relation, DB, y lógica central sin dependencias Qt
│   ├── interpreter/      # Lexer, Parser, Evaluator, AST
│   │   ├── lexer.py
│   │   ├── parser.py
│   │   ├── evaluator.py
│   │   └── rast.py       # Nodos del AST
│   ├── gui/              # Interfaz PyQt6
│   │   ├── services/     # DatabaseService, QueryService
│   │   ├── dialogs/      # Diálogos
│   │   └── theme/        # Temas y colores
│   ├── cli/              # Modo terminal (REPL)
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── gui/
├── docs/
└── pyproject.toml
```

!!! note "Regla importante"
    `core/` e `interpreter/` son Python puro, sin imports de PyQt6. Todo lo que dependa de Qt va en `gui/`.

---

## Hacer cambios

1. Hacer fork del repositorio
2. Crear una rama: `git checkout -b feature/mi-feature`
3. Hacer los cambios y agregar tests
4. Ejecutar los tests: `uv run pytest`
5. Abrir un Pull Request

---

## Reportar bugs

Abrir un issue en [GitHub](https://github.com/centaurialpha/pireal/issues) con:

- Qué hiciste
- Qué esperabas que pasara
- Qué pasó realmente
- Tu sistema operativo y versión de Pireal

---

## Construir la documentación localmente

```bash
uv sync --group docs
uv run mkdocs serve
```

Abrí [http://localhost:8000](http://localhost:8000). La documentación se reconstruye automáticamente al editar archivos.
