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

from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from pireal.core.relation import Relation

PAGER_THRESHOLD = 20


def relation_to_table(relation: Relation) -> Table:
    cardinality = relation.cardinality()
    noun = "tuple" if cardinality == 1 else "tuples"
    table = Table(
        title=f"[bold]{relation.name}[/bold]  [dim]({cardinality} {noun})[/dim]",
        box=box.SIMPLE_HEAD,
        show_header=True,
        header_style="bold cyan",
        title_justify="left",
    )
    for col in relation.header:
        table.add_column(col)
    for row in sorted(relation.content):
        table.add_row(*row)
    return table


def error_panel(message: str) -> Panel:
    return Panel(
        Text(message, style="red"),
        title="[bold red]Error[/bold red]",
        border_style="red",
        padding=(0, 1),
    )


def render_welcome(console: Console, db_path: Path, relations: dict[str, Relation]) -> None:
    console.print()
    console.print(
        Panel(
            f"[bold]πireal[/bold]  -  Terminal Mode\n[dim]{db_path.name}[/dim]",
            border_style="blue",
            padding=(0, 2),
        )
    )
    render_summary(console, relations)


def render_help(console: Console) -> None:
    console.print(
        Panel(
            "  [cyan]\\r[/cyan]          list loaded relations\n"
            "  [cyan]\\r nombre[/cyan]   show relation (pager if large)\n"
            "  [cyan]\\h[/cyan]          this help\n"
            "  [cyan]exit[/cyan]         quit  [dim](also: quit, :q, Ctrl+D)[/dim]",
            title="[dim]commands[/dim]",
            border_style="dim",
            padding=(0, 1),
        )
    )


def render_summary(console: Console, relations: dict[str, Relation]) -> None:
    names = "  ".join(f"[cyan]{n}[/cyan]" for n in relations)
    console.print(f"\n  Relations: {names}\n")
    for name, rel in relations.items():
        console.print(f"  [cyan]{name}[/cyan]  [dim]{rel.cardinality()} tuples - {rel.degree()} attrs[/dim]")
    console.print()


def render_relation(console: Console, relation: Relation) -> None:
    table = relation_to_table(relation)
    if relation.cardinality() > PAGER_THRESHOLD:
        with console.pager():
            console.print(table)
    else:
        console.print(table)
