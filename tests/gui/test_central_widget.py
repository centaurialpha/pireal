import pytest

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from pireal.core.db import DB
from pireal.gui.central_widget import CentralWidget
from pireal.gui.dialogs import DBInputDialog


@pytest.fixture
def central_widget_fixture(qtbot):
    w = CentralWidget(parent=None)
    w._recent_dbs = []
    qtbot.addWidget(w)
    return w


@pytest.mark.gui
@pytest.mark.parametrize(
    'dbs, expected_dbs',
    [
        (['p1', 'p2', 'p1'], ['p1', 'p2']),
        (['p1', 'p1', 'p1'], ['p1'])
    ]
)
def test_remember_database(central_widget_fixture, dbs, expected_dbs):
    for db_path in dbs:
        central_widget_fixture.remember_recent_database(db_path)
    assert central_widget_fixture.recent_databases == expected_dbs


@pytest.mark.gui
def test_open_database(central_widget_fixture, qtbot, monkeypatch, mocker):
    monkeypatch.setattr(
        QFileDialog, 'getOpenFileName', lambda *args: ('algo', None))

    mocker.patch.object(DB, 'from_file')

    with qtbot.waitSignal(central_widget_fixture.dbOpened) as blocker:
        central_widget_fixture.open_database()

        assert blocker.signal_triggered

    assert central_widget_fixture.has_db()
    assert central_widget_fixture._stacked.count() == 1


@pytest.mark.gui
def test_open_database_fail(central_widget_fixture, qtbot, monkeypatch, mocker):
    db_filename = 'not_exist.pdb'
    mocker.patch.object(DB, 'from_file', side_effect=IOError)
    monkeypatch.setattr(QMessageBox, 'critical', lambda *args: QMessageBox.Yes)

    with qtbot.waitSignal(central_widget_fixture.dbOpened, raising=False) as blocker:
        central_widget_fixture.open_database(filename=db_filename)

        assert not blocker.signal_triggered

    assert not central_widget_fixture.has_db()
    assert central_widget_fixture._stacked.count() == 0


@pytest.mark.gui
def test_create_database(central_widget_fixture, monkeypatch, mocker):
    test_db_path = 'path/to/db/example.pdb'
    monkeypatch.setattr(
        DBInputDialog, 'ask_db_name', lambda parent=central_widget_fixture: test_db_path)

    central_widget_fixture.create_database()

    assert central_widget_fixture.has_db()
    assert central_widget_fixture.db_panel.db._path == test_db_path
    assert central_widget_fixture._stacked.count() == 1
