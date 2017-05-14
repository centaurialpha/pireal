import os
from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout
)
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import (
    QUrl,
    Qt
)
from src.core import settings


class MessageError(QDialog):
    def __init__(self, parent=None):
        super(MessageError, self).__init__(parent,
                                           Qt.Dialog | Qt.FramelessWindowHint)
        self._parent = parent
        self.setModal(True)
        self.setFixedHeight(150)
        self.setFixedWidth(350)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        view = QQuickView()
        qml = os.path.join(settings.QML_PATH, "MessageError.qml")
        view.setSource(QUrl.fromLocalFile(qml))
        view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.widget = QWidget.createWindowContainer(view)
        box.addWidget(self.widget)

        self._root = view.rootObject()
        self._root.close.connect(self.close)

    def show_msg(self, msg, syntax_error=True):
        self._root.setMessageType(syntax_error)
        self._root.setMessage(msg)

    def showEvent(self, event):
        QDialog.showEvent(self, event)
        # Center
        pos_x = self._parent.width() / 2 - (self.width() / 2)
        pos_y = self._parent.height() / 2 - (self.height() / 2)
        self.move(pos_x, pos_y)
