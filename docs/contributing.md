# Contribuir

Las contribuciones son bienvenidas y apreciadas. Ya sea un reporte de bug, una funcionalidad nueva, o una corrección en la documentación — todo ayuda.

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

---

## Estructura del proyecto

```
pireal/
├── src/pireal/
│   ├── core/          # Modelo de Relation y lógica central
│   ├── interpreter/   # Scanner, Lexer, Parser, Evaluator
│   │   ├── scanner.py
│   │   ├── lexer.py
│   │   ├── parser.py
│   │   ├── evaluator.py
│   │   └── rast.py    # Definición de nodos del AST
│   ├── gui/           # Interfaz PyQt6
│   └── main.py
├── tests/
│   ├── unit/
│   └── integration/
├── docs/              # Esta documentación
└── pyproject.toml
```

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
- Tu sistema operativo y versión de Python

---

## Construir la documentación localmente

Agregar el grupo de docs al `pyproject.toml`:

```toml
[dependency-groups]
docs = [
    "mkdocs-material>=9.5",
]
```

Luego:

```bash
uv sync --group docs
uv run mkdocs serve
```

Abrí [http://localhost:8000](http://localhost:8000). La documentación se reconstruye automáticamente al editar archivos.
