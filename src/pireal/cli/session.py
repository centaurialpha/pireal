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

from __future__ import annotations

import readline  # noqa: F401, activa historial/flechas en input() en Linux/macOS
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

from pireal.cli.display import (
    error_panel,
    relation_to_table,
    render_help,
    render_relation,
    render_welcome,
)
from pireal.core.pireal_file import File
from pireal.core.relation import Relation
from pireal.core.relation_loader import load_relations
from pireal.interpreter.evaluator import (
    Evaluator,
    UndefinedRelationError,
)
from pireal.interpreter.exceptions import InterpreterError
from pireal.interpreter.parser import parse
from pireal.utils import sanitize_data


def _load_relations(db_path: Path) -> dict[str, Relation]:
    file = File(str(db_path))
    data = sanitize_data(file.read())
    return {relation.name: relation for relation in load_relations(data)}


def _execute_query(
    query_text: str,
    session_relations: dict[str, Relation],
) -> tuple[dict[str, Relation], Exception | None]:
    try:
        tree = parse(query_text)
        results = Evaluator(session_relations).evaluate(tree)
        return results, None
    except (InterpreterError, UndefinedRelationError, SyntaxError) as err:
        return {}, err


def run(db_path: Path | None = None) -> int:
    console = Console()

    if db_path is None:
        raw = Prompt.ask("[bold blue]Database path[/bold blue]")
        db_path = Path(raw.strip())

    if not db_path.exists():
        console.print(error_panel(f"File not found: '{db_path}'"))
        return 1

    try:
        session_relations = _load_relations(db_path)
    except Exception as err:
        console.print(error_panel(f"Could not load database: {err}"))
        return 1

    render_welcome(console, db_path, session_relations)

    _repl_loop(console, session_relations)
    return 0


def _repl_loop(console: Console, session_relations: dict[str, Relation]) -> None:
    buffer: list[str] = []

    while True:
        prompt = "pireal> " if not buffer else "     …  "
        try:
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]EOF[/dim]")
            break

        stripped = line.strip()

        if not buffer:
            match stripped:
                case "exit" | "quit" | "chau" | ":q":
                    console.print("[dim]Bye![/dim]")
                    break
                case r"\h":
                    render_help(console)
                    continue
                case string if string.startswith(r"\r"):
                    _handle_show_relation(console, session_relations, string)
                    continue
                case "":
                    continue

        buffer.append(stripped)
        full = " ".join(buffer)

        # ejecutar cuando haya al menos un ;
        if ";" not in full:
            continue

        buffer.clear()
        results, err = _execute_query(full, session_relations)

        if err is not None:
            console.print(error_panel(str(err)))
            continue

        for name, relation in results.items():
            relation.name = name
            session_relations[name] = relation
            console.print(relation_to_table(relation))


def _handle_show_relation(
    console: Console,
    session_relations: dict[str, Relation],
    command: str,
) -> None:
    parts = command.split(maxsplit=1)
    if len(parts) == 1:
        _list_relations(console, session_relations)
        return
    name = parts[1].strip()
    relation = session_relations.get(name)
    if relation is None:
        console.print(error_panel(f"Relation '{name}' not found."))
        return
    render_relation(console, relation)


def _list_relations(console: Console, session_relations: dict[str, Relation]) -> None:
    if not session_relations:
        console.print("[dim]No relations loaded.[/dim]")
        return
    for name, rel in session_relations.items():
        console.print(f"  [cyan]{name}[/cyan]  [dim]{rel.cardinality()} tuples, {rel.degree()} attrs[/dim]")
