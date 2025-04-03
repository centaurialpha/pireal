from PyQt6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

from pireal.gui.database_container import DatabaseContainer
from pireal.registry import Registry
from pireal.utils import sanitize_data


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        box = QVBoxLayout(self)

        self.stack = QStackedWidget()
        box.addWidget(self.stack)

    def create_database(self):
        database_widget = Registry.get("database-container", DatabaseContainer)
        self.stack.setCurrentWidget(database_widget)

    def open_database(self, filename):
        """
        - si ya hay una db abierta, avisar y no hacer nada.
        - si no se proporciona un archivo, abrir el file dialog para seleccionar.
        - leer el archivo y sanitizar la data.
        - crear la db en el database container
        - agregar el container al stack
        - mostrar un mensaje en la toolbar del archivo abierto.
        - actualizar el titulo de la ventana con el nombre del archivo.
        - agregar la db a la lista de recientes.
        """
        with open(filename) as fp:
            content = sanitize_data(fp.read())

        database_container = Registry.get("database-container", DatabaseContainer)
        database_container.create_database(content)
        self.stack.setCurrentWidget(database_container)

    def open_query(self, filename="", remember=True):
        self.new_query(filename)


    def new_query(self, filename: str):
        database_widget = Registry.get("database-container", DatabaseContainer)
        database_widget.new_query(filename)

    def add_widget(self, widget):
        index = self.stack.addWidget(widget)
        self.stack.setCurrentIndex(index)
