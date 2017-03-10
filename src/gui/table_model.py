from PyQt5.QtCore import (
    QAbstractTableModel,
    Qt
)


class Model(QAbstractTableModel):
    """ Modelo """

    def __init__(self, relation_obj):
        QAbstractTableModel.__init__(self)
        self.__data = relation_obj

    def rowCount(self, parent):
        return len(self.__data.content)

    def columnCount(self, parent):
        return len(self.__data.header)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return list(self.__data.content)[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            return self.__data.header[section]
