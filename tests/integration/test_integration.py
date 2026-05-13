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

from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

import pytest
from PyQt6.QtWidgets import QStackedWidget

from pireal.core.db import DB
from pireal.gui.controller import Controller
from pireal.gui.database_container import DatabaseContainer
from pireal.gui.lateral_widget import LateralWidget
from pireal.gui.menu import MenuBuilder
from pireal.gui.query_widget import QueryWidget
from pireal.gui.start_page import StartPage
from pireal.registry import Registry
from pireal.resources import sample

pytestmark = pytest.mark.integration


@dataclass
class App:
    controller: Controller
    db: DB
    lateral: LateralWidget
    query_widget: QueryWidget
    menu_builder: MenuBuilder


@pytest.fixture()
def app(tmp_path, qtbot):
    """
    Levanta el stack completo de Pireal en un entorno aislado:
    - QSettings en tmp_path
    - Registry limpio
    - offscreen
    """
    settings_file = tmp_path / "settings.ini"

    with (
        patch("pireal.settings.CONFIG_FILE", settings_file),
        patch("pireal.dirs.DATA_SETTINGS", settings_file),
        patch("pireal.gui.controller.DATA_SETTINGS", settings_file),
        patch("pireal.gui.database_container.DATA_SETTINGS", settings_file),
    ):
        from pireal.settings import settings

        settings._loaded = False
        settings.load()

        from PyQt6.QtWidgets import QMainWindow

        from pireal.core.db import DB
        from pireal.gui.controller import Controller
        from pireal.gui.lateral_widget import LateralWidget
        from pireal.gui.menu import MenuBuilder
        from pireal.gui.query_widget import QueryWidget
        from pireal.gui.right_pane import RightPane
        from pireal.gui.status_bar import StatusBar
        from pireal.gui.table_widget import TableWidget

        Registry._components.clear()

        def reg(name, widget):
            if hasattr(widget, "show"):
                qtbot.addWidget(widget)
            Registry.register(name, widget)
            return widget

        db = reg("db", DB())
        lateral = reg("lateral-widget", LateralWidget())
        _ = reg("table-widget", TableWidget())
        qw = reg("query-widget", QueryWidget())
        _ = reg("status-bar", StatusBar())
        _ = reg("right-pane", RightPane())
        _ = reg("database-container", DatabaseContainer())
        _ = reg("start-page", StartPage())
        ctrl = reg("controller", Controller())

        main_window = QMainWindow()
        qtbot.addWidget(main_window)
        Registry.register("pireal", main_window)

        menu_builder = MenuBuilder(main_window, ctrl)
        menu_builder.build()
        main_window._mb = menu_builder  # ty: ignore[unresolved-attribute]

        ctrl.add_widget(Registry.get("start-page", StartPage))

        yield App(
            controller=ctrl,
            db=db,
            lateral=lateral,
            query_widget=qw,
            menu_builder=menu_builder,
        )

        Registry._components.clear()
        settings._loaded = False


def _pump(qtbot, ms: int = 50) -> None:
    qtbot.wait(ms)


def _open_example(app: App, qtbot) -> None:
    app.controller.open_database(sample("database.pdb"))
    app.controller.open_query(sample("queries.pqf"))
    _pump(qtbot)


def test_start_page_shown_at_startup(app):
    stack: QStackedWidget = app.controller._stack
    assert isinstance(stack.currentWidget(), StartPage)


def test_db_inactive_at_startup(app):
    assert not app.db.is_active


def test_no_recents_on_first_run(app):
    assert not app.controller.recent_databases


def test_db_dependent_actions_disabled_without_db(app):
    for action in app.menu_builder.db_dependent_actions:
        assert not action.isEnabled(), f"'{action.text()}' debería estar desactivada sin DB"


def test_open_db_activates_db(app, qtbot):
    app.controller.open_database(sample("database.pdb"))
    _pump(qtbot)
    assert app.db.is_active


def test_open_db_loads_relations_in_lateral(app, qtbot):
    app.controller.open_database(sample("database.pdb"))
    _pump(qtbot)
    assert app.lateral._relations_model.rowCount() > 0


def test_open_db_enables_menu_actions(app, qtbot):
    app.controller.open_database(sample("database.pdb"))
    _pump(qtbot)
    for action in app.menu_builder.db_dependent_actions:
        assert action.isEnabled(), f"'{action.text()}' debería estar activa con DB abierta"


def test_open_db_shows_database_container(app, qtbot):
    app.controller.open_database(sample("database.pdb"))
    _pump(qtbot)
    stack: QStackedWidget = app.controller._stack
    assert isinstance(stack.currentWidget(), DatabaseContainer)


def test_close_db_returns_to_start_page(app, qtbot):
    app.controller.open_database(sample("database.pdb"))
    _pump(qtbot)
    app.controller.close_database()
    _pump(qtbot)
    stack: QStackedWidget = app.controller._stack
    assert isinstance(stack.currentWidget(), StartPage)


def test_close_db_disables_menu_actions(app, qtbot):
    app.controller.open_database(sample("database.pdb"))
    _pump(qtbot)
    app.controller.close_database()
    _pump(qtbot)
    for action in app.menu_builder.db_dependent_actions:
        assert not action.isEnabled(), f"'{action.text()}' debería estar desactivada tras cerrar DB"


def test_example_not_added_to_recents(app, qtbot):
    app.controller.open_database(sample("database.pdb"))
    _pump(qtbot)
    assert not app.controller.recent_databases


def test_real_db_added_to_recents(app, qtbot, tmp_path):
    db_file = tmp_path / "mydb.pdb"
    db_file.write_text("@t:id\n1\n", encoding="utf-8")
    app.controller.open_database(str(db_file))
    _pump(qtbot)
    assert any(Path(path).resolve() == db_file.resolve() for path in app.controller.recent_databases)


def test_open_query_without_db_does_nothing(app, qtbot):
    app.controller.open_query(sample("queries.pqf"))
    _pump(qtbot)
    assert app.query_widget.current_editor() is None


def test_open_query_with_db_creates_editor(app, qtbot):
    _open_example(app, qtbot)
    assert app.query_widget.current_editor() is not None


def test_execute_queries_produces_results(app, qtbot):
    _open_example(app, qtbot)
    app.controller.execute_queries()
    _pump(qtbot, ms=200)
    assert app.lateral._results_model.rowCount() > 0


def test_execute_without_db_does_not_crash(app, qtbot):
    app.controller.execute_queries()
    _pump(qtbot)


def test_close_db_clears_editors(app, qtbot):
    _open_example(app, qtbot)
    app.controller.close_database()
    _pump(qtbot)
    assert app.query_widget.current_editor() is None


def test_add_relations_extends_existing(app, qtbot):
    from pireal.utils import sanitize_data

    app.controller.open_database(sample("database.pdb"))
    _pump(qtbot)

    before = app.lateral._relations_model.rowCount()
    dc = Registry.get("database-container", DatabaseContainer)
    dc.add_relations(sanitize_data("@extra:id,val\n1,x\n"))
    _pump(qtbot)

    assert app.lateral._relations_model.rowCount() == before + 1
    assert app.db.modified


def test_open_nonexistent_db_does_not_activate(app, qtbot):
    with patch("pireal.gui.services.database_service.QMessageBox.warning"):
        app.controller.open_database("/no/existe/db.pdb")
    _pump(qtbot)
    assert not app.db.is_active
