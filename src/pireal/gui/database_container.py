from typing import Dict

from PyQt6.QtCore import QSettings, Qt, pyqtSlot
from PyQt6.QtWidgets import QSplitter

from pireal.core.db import DB
from pireal.core.pireal_file import File
from pireal.core.relation import Relation
from pireal.dirs import DATA_SETTINGS
from pireal.gui.lateral_widget import LateralWidget, RelationItemType
from pireal.gui.model_view_delegate import Delegate, RelationModel, View
from pireal.gui.query_widget import QueryWidget
from pireal.gui.table_widget import TableWidget
from pireal.registry import Registry


def create_view(relation, *, editable=False):
    view = View()
    model = RelationModel(relation)
    model.editable = editable
    view.setModel(model)
    view.setItemDelegate(Delegate())
    return view


class DatabaseContainer(QSplitter):
    def __init__(self, orientation=Qt.Orientation.Horizontal):
        super().__init__(orientation)
        lateral_widget = Registry.get("lateral-widget", LateralWidget)
        table_widget = Registry.get("table-widget", TableWidget)
        query_widget = Registry.get("query-widget", QueryWidget)

        self._vsplitter = QSplitter(Qt.Orientation.Vertical)
        self._vsplitter.addWidget(table_widget)
        self._vsplitter.addWidget(query_widget)

        self.addWidget(lateral_widget)
        self.addWidget(self._vsplitter)

        self._relations: Dict[str, Relation] = {}
        self._database = Registry.get("db", DB)

        lateral_widget.relationClicked.connect(self._on_relation_clicked)

    def create_database(self, data):
        table_widget = Registry.get("table-widget", TableWidget)
        lateral_widget = Registry.get("lateral-widget", LateralWidget)
        for table in data.get("tables"):
            table_name = table.get("name")
            header = table.get("header")
            tuples = table.get("tuples")

            rela = Relation()
            rela.header = header

            for tup in tuples:
                rela.insert(tup)

            # FIXME: feo
            rela.name = table_name

            self._database.load(rela)

            # FIXME: acá se hace un add por lo tanto se modifica la db, utilizar load
            table_widget.add_table_to_workspace(rela)

            lateral_widget.add_item(rela, RelationItemType.Normal)

        self._database.modified = False

    @pyqtSlot(int)
    def _on_relation_clicked(self, row: int):
        table_widget = Registry.get("table-widget", TableWidget)
        table_widget._stacked.setCurrentIndex(row)

    def showEvent(self, a0):
        super().showEvent(a0)
        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        vsizes = qsettings.value("vsplitter_sizes", None)
        if vsizes is not None:
            self._vsplitter.restoreState(vsizes)
        else:
            self._vsplitter.setSizes(
                [round(self.height() / 3), round(self.height() / 6)]
            )
        hsizes = qsettings.value("hsplitter_sizes", None)
        if hsizes is not None:
            self.restoreState(hsizes)
        else:
            self.setSizes([round(self.width() / 10), round(self.width() / 3)])

    def new_query(self, filename: str) -> None:
        query_widget = Registry.get("query-widget", QueryWidget)

        file = File(filename)
        editor = query_widget.create_editor(file)
        if filename:
            content = file.read()
            editor.setText(content)

    def execute_queries(self):
        from pireal.interpreter.parser import parse

        table_widget = Registry.get("table-widget", TableWidget)
        query_widget = Registry.get("query-widget", QueryWidget)
        lateral_widget = Registry.get("lateral-widget", LateralWidget)

        editor = query_widget.current_editor()
        queries = editor.text()

        editor.editor.show_run_cursor()

        # FIXME: probar project cod_curso (inscripto) algo raro.
        # FIXME: borrar y eliminar los items (lateral y table)
        # self._database.clear()
        lateral_widget.clear_results()
        i = table_widget._stacked_results.count()
        while i >= 0:
            widget = table_widget._stacked_results.widget(i)
            if widget is not None:
                table_widget._stacked_results.removeWidget(widget)
                widget.deleteLater()
            i -= 1

        self._database.clear_query_results()
        result = parse(queries)

        for relation_name, expression in result.items():
            new_relation = self._database.eval_query(expression, relation_name)
            table_widget.add_table_to_results(new_relation)
            lateral_widget.add_item(new_relation, RelationItemType.Result)
