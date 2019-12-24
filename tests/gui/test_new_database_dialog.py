import os
import pytest

from pireal.gui.dialogs import DBInputDialog


@pytest.fixture
def db_input_fixture(qtbot, tmp_path):
    db_location = tmp_path / 'test-ask-db-name'
    db_location.mkdir()
    dialog = DBInputDialog()
    qtbot.addWidget(dialog)
    dialog._line_db_location.setText(str(db_location))
    return dialog, db_location


@pytest.mark.gui
def test_ask_db_name(qtbot, db_input_fixture):
    dialog, tmp_db = db_input_fixture
    db_name = 'example'
    expected_db_path = os.path.join(tmp_db, db_name)
    qtbot.keyClicks(dialog._line_db_name, db_name)
    ret, _ = os.path.splitext(dialog.db_path)

    assert ret == expected_db_path
    assert dialog._button_ok.isEnabled()


@pytest.mark.gui
def test_ask_db_name_db_exist(qtbot, db_input_fixture):
    dialog, tmp_db = db_input_fixture
    db = tmp_db / 'esto_existe.pdb'
    db.write_text('some content')
    qtbot.keyClicks(dialog._line_db_name, 'esto_existe')

    assert not dialog._button_ok.isEnabled()
