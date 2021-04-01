# -*- coding: utf-8 -*-
#
# Copyright 2015 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

import logging
import os
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListView,
    QSizePolicy,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QStyle,
)
from PyQt5.QtGui import (
    QPixmap,
)
from PyQt5.QtCore import (
    QAbstractListModel,
    Qt,
    QRect,
    QModelIndex,
    QSettings,
    QTimer,
    pyqtSlot as Slot
)

from pireal.dirs import (
    DATA_SETTINGS,
    EXAMPLES_DIR,
)
from pireal.gui.main_window import Pireal
from pireal import translations as tr

logger = logging.getLogger(__name__)


class RecentDBModel(QAbstractListModel):

    def __init__(self, data):
        super().__init__()
        self._items = data

    def rowCount(self, parent=None):
        return len(self._items)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        item = self._items[index.row()]
        if role == Qt.DisplayRole:
            return item[0]
        elif role == Qt.UserRole:
            return item[1]
        return None


class RecentDBDelegate(QStyledItemDelegate):
    """Custom delegate that show database name and database path
    in same item"""

    def paint(self, painter, option, index):
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)

        db_name = index.model().data(index, Qt.DisplayRole)
        db_path = index.model().data(index, Qt.UserRole)

        opt.text = ''
        opt.widget.style().drawControl(QStyle.CE_ItemViewItem, opt, painter, opt.widget)

        rect = opt.rect

        rect = rect.adjusted(5, 3, 5, -3)
        painter.save()

        # Draw database name
        font = painter.font()
        font.setBold(True)
        font.setPointSize(12)
        painter.setFont(font)
        painter.drawText(
            QRect(rect.left(), rect.top(), rect.width(), rect.height() / 2),
            opt.displayAlignment, db_name)

        painter.restore()

        # Draw path name
        painter.drawText(
            QRect(rect.left(), rect.top() + rect.height() / 2, rect.width(), rect.height() / 2),
            opt.displayAlignment, db_path)

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(size.height() * 2.5)
        return size


class StartPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        qsettings = QSettings(str(DATA_SETTINGS), QSettings.IniFormat)

        main_layout = QVBoxLayout(self)
        title_lbl = QLabel('<b><font color="#1565c0">π</font></b>real')
        font = title_lbl.font()
        font.setPointSize(42)
        title_lbl.setFont(font)

        subtitle_lbl = QLabel('free and open source Relational Algebra Interpreter')
        font = subtitle_lbl.font()
        font.setPointSize(14)
        subtitle_lbl.setFont(font)

        # Buttons
        hbox_btn = QHBoxLayout()
        btn_open_db = QPushButton(tr.TR_OPEN_DB)
        btn_open_db.setMinimumSize(150, 0)
        btn_open_db.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        btn_new_db = QPushButton(tr.TR_NEW_DB)
        btn_new_db.setMinimumSize(150, 0)
        btn_new_db.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        btn_example = QPushButton(tr.TR_EXAMPLE_DB)
        btn_example.setMinimumSize(150, 0)
        btn_example.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        hbox_btn.addStretch()
        hbox_btn.addWidget(btn_open_db)
        hbox_btn.addWidget(btn_new_db)
        hbox_btn.addWidget(btn_example)
        hbox_btn.addStretch()

        # List
        frame_recent_dbs = QFrame()
        frame_recent_dbs.setFrameShape(QFrame.StyledPanel)
        frame_recent_dbs.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        vbox_recent_dbs = QVBoxLayout(frame_recent_dbs)
        vbox_recent_dbs.addWidget(QLabel('Recent Databases'), alignment=Qt.AlignHCenter)
        self._recent_dbs_list = QListView()
        self._recent_dbs_list.setMinimumWidth(550)
        vbox_recent_dbs.addWidget(self._recent_dbs_list, alignment=Qt.AlignHCenter)
        model_data = []
        for recent_db in qsettings.value('recent_databases', type=list):
            name = os.path.splitext(os.path.basename(recent_db))[0]
            model_data.append((name, recent_db))
        self._model = RecentDBModel(model_data)
        self._recent_dbs_list.setModel(self._model)
        self._recent_dbs_list.setItemDelegate(RecentDBDelegate())

        # Footer
        hbox_footer = QHBoxLayout()
        powered_by_lbl = QLabel('Powered by: ')
        hbox_footer.addWidget(powered_by_lbl)
        python_logo = QPixmap(':img/python')
        python_logo_lbl = QLabel()
        python_logo_lbl.setPixmap(python_logo)
        hbox_footer.addWidget(python_logo_lbl, alignment=Qt.AlignLeft)
        qt_logo = QPixmap(':img/bwqt')
        qt_logo_lbl = QLabel()
        qt_logo_lbl.setPixmap(qt_logo)
        hbox_footer.addWidget(qt_logo_lbl, alignment=Qt.AlignLeft)
        hbox_footer.addStretch(1)

        now = datetime.now()
        copyright_lbl = QLabel(
            f'Copyright © 2015-{now.year} Gabriel Acosta. '
            f'Pireal is distributed under the terms of the GNU GPLv3+ copyleft license')
        hbox_footer.addWidget(copyright_lbl)

        main_layout.addStretch(1)
        main_layout.addWidget(title_lbl, alignment=Qt.AlignHCenter)
        main_layout.addWidget(subtitle_lbl, alignment=Qt.AlignHCenter)
        main_layout.addLayout(hbox_btn)
        main_layout.addWidget(frame_recent_dbs, alignment=Qt.AlignHCenter)
        main_layout.addStretch(1)
        main_layout.addStretch(1)
        main_layout.addLayout(hbox_footer)

        self._recent_dbs_list.doubleClicked.connect(self._on_listview_item_double_clicked)
        btn_open_db.clicked.connect(self._open_database)
        btn_new_db.clicked.connect(self._new_database)
        btn_example.clicked.connect(self._open_example)

    def _new_database(self):
        central_widget = Pireal.get_service('central')
        central_widget.create_database()

    def _open_database(self, path=None):
        central_widget = Pireal.get_service('central')
        central_widget.open_database(path)

    def _open_example(self):
        central_widget = Pireal.get_service('central')
        logger.info("DATABASE: %s", str(EXAMPLES_DIR / 'database.pdb'))
        central_widget.open_database(str(EXAMPLES_DIR / 'database.pdb'))
        central_widget.open_query(str(EXAMPLES_DIR / 'queries.pqf'))

        QTimer.singleShot(1300, central_widget.execute_queries)

    @Slot(QModelIndex)
    def _on_listview_item_double_clicked(self, index):
        path = self._model.data(index, role=Qt.UserRole)
        if path is not None:
            self._open_database(path)
