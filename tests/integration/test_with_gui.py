# from pathlib import Path
# from unittest import mock

# import pytest

# from pireal.core.db import DB
# from pireal.core.interpreter import parse

# from pireal.gui.main_window import Pireal
# from pireal.gui.central_widget import CentralWidget
# from pireal.gui.dialogs import DBInputDialog
# from pireal.gui.dialogs import NewRelationDialog


# SAMPLES = Path().cwd() / 'samples'
# SAMPLE_PDB_PATH = SAMPLES / 'database.pdb'
# SAMPLE_PDB_WINDOWS_PATH = SAMPLES / 'database_windows.pdb'
# QUERY_PATH = SAMPLES / 'queries.pqf'


# @pytest.mark.integration
# @pytest.mark.parametrize(
#     'db_path',
#     [SAMPLE_PDB_PATH, ]
# )
# def test_full_cycle_with_gui(qtbot, monkeypatch, tmpdir, db_path):
#     """
#     - Create new db
#     - add relations
#     - save db
#     - Open db
#     - Create query file
#     - Save query file
#     - Close query file
#     - Re open query file
#     - Execute queries
#     """
#     test_db_file = tmpdir.join('mi_db.pdb')
#     main_window = Pireal(check_updates=False)
#     qtbot.addWidget(main_window)
#     central_widget = CentralWidget(parent=main_window)
#     qtbot.addWidget(central_widget)

#     monkeypatch.setattr(
#         DBInputDialog, 'ask_db_name', lambda parent=central_widget: test_db_file)

#     # Create new DB
#     central_widget.create_database()

#     # Add relation
#     rela_dialog = NewRelationDialog(parent=central_widget)
#     qtbot.addWidget(rela_dialog)
#     qtbot.keyClicks(rela_dialog.line_relation_name, 'people')
