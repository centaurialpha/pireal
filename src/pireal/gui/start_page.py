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
from typing import Optional

from PyQt6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QRect,
    QSettings,
    Qt,
    QTimer,
)
from PyQt6.QtCore import (
    pyqtSlot as Slot,
)
from PyQt6.QtGui import QColor, QPainter, QPalette, QPen, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListView,
    QPushButton,
    QSizePolicy,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QVBoxLayout,
    QWidget,
)

from pireal import translations as tr
from pireal.dirs import DATA_SETTINGS, EXAMPLES_DIR
from pireal.gui.controller import Controller
from pireal.registry import Registry

logger = logging.getLogger(__name__)


class RecentDBModel(QAbstractListModel):
    def __init__(self, data):
        super().__init__()
        self._items = data

    def rowCount(self, parent=None):
        _ = parent
        return len(self._items)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        item = self._items[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return item[0]
        elif role == Qt.ItemDataRole.UserRole:
            return item[1]
        return None


class RecentDBDelegate(QStyledItemDelegate):
    """
    Custom delegate that show database name and database path
    in same item
    """

    def paint(
        self,
        painter: Optional[QPainter],
        option: "QStyleOptionViewItem",
        index: QModelIndex,
    ) -> None:
        print("AAAAAAAAAAAA")
        if painter is None:
            return

        model = index.model()
        if model is None:
            return

        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)

        db_name = model.data(index, Qt.ItemDataRole.DisplayRole)
        db_path = model.data(index, Qt.ItemDataRole.UserRole)

        if not db_name:
            return

        style = opt.widget.style()
        opt.text = ""
        if style is not None:
            style.drawControl(
                QStyle.ControlElement.CE_ItemViewItem, opt, painter, opt.widget
            )

        rect = option.rect
        item_rect = rect.adjusted(0, 0, 0, 0)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Draw background
        # self._draw_background(painter, item_rect, opt.state)
        # Draw content
        content_rect = item_rect.adjusted(8, 3, -8, -3)
        self._draw_content(painter, content_rect, db_name, db_path, option.state)
        painter.restore()

    def _draw_background(self, painter, rect, state):
        # if state & QStyle.StateFlag.State_Selected:
        #     # bg_color = QColor(theme_manager.get_color("Highlight"))
        #     # border_color = QColor(theme_manager.get_color("Shadow"))
        # elif state & QStyle.StateFlag.State_MouseOver:
        #     bg_color = QColor(theme_manager.get_color("AlternateBase"))
        #     border_color = QColor(theme_manager.get_color("Mid"))
        # else:
        #     bg_color = QColor(theme_manager.get_color("Base"))
        #     border_color = QColor(theme_manager.get_color("Dark"))

        # # painter.setBrush(QBrush(bg_color))
        # pen = QPen(border_color)
        # painter.setPen(pen)

        painter.drawRect(rect)

    def _draw_content(self, painter, rect, title, subtitle, state):
        """Dibuja el contenido usando roles estándar de Qt."""

        # if state & QStyle.StateFlag.State_Selected:
        #     title_color = QColor(theme_manager.get_color("HighlightedText"))
        # else:
        #     title_color = QColor(theme_manager.get_color("Text"))

        # subtitle_color = QColor(theme_manager.get_color("Light"))

        font = painter.font()
        font.setBold(True)
        font.setPointSize(12)
        painter.setFont(font)
        # painter.setPen(QPen(title_color))

        title_height = rect.height() // 2
        subtitle_height = rect.height() - title_height

        title_rect = QRect(rect.left(), rect.top(), rect.width(), title_height)
        painter.drawText(
            title_rect,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            title,
        )

        font.setBold(False)
        font.setPointSize(10)
        painter.setFont(font)
        # painter.setPen(QPen(subtitle_color))

        subtitle_rect = QRect(
            rect.left(), rect.top() + title_height, rect.width(), subtitle_height
        )

        metrics = painter.fontMetrics()
        elided_subtitle = metrics.elidedText(
            subtitle,
            Qt.TextElideMode.ElideLeft,
            subtitle_rect.width(),
        )

        painter.drawText(
            subtitle_rect,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            elided_subtitle,
        )

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(int(size.height() * 3.0))
        return size


class RecentDatabasesView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        palette = self.palette()
        # palette.setColor(
        #     QPalette.ColorRole.Window, QColor(theme_manager.get_color("AlternateBase"))
        # )
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        vbox = QVBoxLayout(self)
        label = QLabel("Recent Databases")
        vbox.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._recent_dbs_list = QListView()
        pal = self._recent_dbs_list.palette()
        # pal.setColor(pal.ColorRole.Base, QColor(theme_manager.get_color("Window")))
        self._recent_dbs_list.setPalette(pal)
        self._recent_dbs_list.setAutoFillBackground(True)
        self._recent_dbs_list.setFrameShape(QListView.Shape.NoFrame)
        self._recent_dbs_list.setVerticalScrollMode(QListView.ScrollMode.ScrollPerPixel)
        self._recent_dbs_list.setSelectionMode(QListView.SelectionMode.SingleSelection)
        self._recent_dbs_list.setMinimumWidth(550)

        vbox.addWidget(self._recent_dbs_list, alignment=Qt.AlignmentFlag.AlignHCenter)

        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)

        model_data = []
        for recent_db in qsettings.value("recent_databases", type=list):
            name = os.path.splitext(os.path.basename(recent_db))[0]
            model_data.append((name, recent_db))

        self.model = RecentDBModel(model_data)
        self._recent_dbs_list.setModel(self.model)
        self._recent_dbs_list.setItemDelegate(RecentDBDelegate())


class StartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        title_lbl = QLabel('<b><font color="#1565c0">π</font></b>real')
        font = title_lbl.font()
        font.setPointSize(42)
        title_lbl.setFont(font)

        subtitle_lbl = QLabel("free and open source Relational Algebra Interpreter")
        font = subtitle_lbl.font()
        font.setPointSize(14)
        subtitle_lbl.setFont(font)

        # Buttons
        hbox_btn = QHBoxLayout()
        btn_open_db = QPushButton(tr.TR_OPEN_DB)
        btn_open_db.setMinimumSize(150, 0)
        btn_open_db.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        btn_new_db = QPushButton(tr.TR_NEW_DB)
        btn_new_db.setMinimumSize(150, 0)
        btn_new_db.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        btn_example = QPushButton(tr.TR_EXAMPLE_DB)
        btn_example.setMinimumSize(150, 0)
        btn_example.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )

        hbox_btn.addStretch()
        hbox_btn.addWidget(btn_open_db)
        hbox_btn.addWidget(btn_new_db)
        hbox_btn.addWidget(btn_example)
        hbox_btn.addStretch()

        # List
        self._recent_databases_view = RecentDatabasesView()
        # pal = frame_recent_dbs.palette()
        # pal.setColor(pal.ColorRole.Window, QColor("#282828"))
        # frame_recent_dbs.setPalette(pal)
        # frame_recent_dbs.setFrameShape(QFrame.Shape.StyledPanel)
        # frame_recent_dbs.setSizePolicy(
        #     QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        # )
        # frame_recent_dbs.setAutoFillBackground(True)

        # Footer
        hbox_footer = QHBoxLayout()
        powered_by_lbl = QLabel("Powered by: ")
        hbox_footer.addWidget(powered_by_lbl)
        python_logo = QPixmap("icons:python-logo.png")
        python_logo_lbl = QLabel()
        python_logo_lbl.setPixmap(python_logo)
        hbox_footer.addWidget(python_logo_lbl, alignment=Qt.AlignmentFlag.AlignLeft)
        qt_logo = QPixmap("icons:bwqt.png")
        qt_logo_lbl = QLabel()
        qt_logo_lbl.setPixmap(qt_logo)
        hbox_footer.addWidget(qt_logo_lbl, alignment=Qt.AlignmentFlag.AlignLeft)
        hbox_footer.addStretch(1)

        now = datetime.now()
        copyright_lbl = QLabel(
            f"Copyright © 2015-{now.year} Gabriel Acosta. "
            f"Pireal is distributed under the terms of the GNU GPLv3+ copyleft license"
        )
        hbox_footer.addWidget(copyright_lbl)

        main_layout.addStretch(1)
        main_layout.addWidget(title_lbl, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(subtitle_lbl, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.addLayout(hbox_btn)
        main_layout.addWidget(
            self._recent_databases_view, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        main_layout.addStretch(1)
        main_layout.addStretch(1)
        main_layout.addLayout(hbox_footer)

        self._recent_databases_view._recent_dbs_list.doubleClicked.connect(
            self._on_listview_item_double_clicked
        )
        btn_open_db.clicked.connect(self._open_database)
        btn_new_db.clicked.connect(self._new_database)
        btn_example.clicked.connect(self._open_example)

    def _new_database(self):
        controller = Registry.get("controller", Controller)
        controller.create_database()

    def _open_database(self, path: str):
        controller = Registry.get("controller", Controller)
        controller.open_database(path)

    def _open_example(self):
        controller = Registry.get("controller", Controller)
        controller.open_database(EXAMPLES_DIR / "database.pdb")
        controller.open_query(str(EXAMPLES_DIR / "queries.pqf"))

        QTimer.singleShot(1300, controller.execute_queries)

    @Slot(QModelIndex)
    def _on_listview_item_double_clicked(self, index):
        path = self._recent_databases_view.model.data(
            index, role=Qt.ItemDataRole.UserRole
        )
        if path is not None:
            self._open_database(path)
