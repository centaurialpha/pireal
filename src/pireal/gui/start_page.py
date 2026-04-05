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
from pathlib import Path

from PyQt6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QRect,
    QSettings,
    Qt,
    QTimer,
    pyqtSignal,
    pyqtSlot as Slot,
)
from PyQt6.QtGui import QFont, QPainter, QPalette, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
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
from pireal.dirs import DATA_SETTINGS
from pireal.gui.controller import Controller
from pireal.registry import Registry
from pireal.resources import sample

logger = logging.getLogger(__name__)


class RecentDBModel(QAbstractListModel):
    def __init__(self, data: list[tuple[str, str]]):
        super().__init__()
        self._items = data

    def rowCount(self, parent=QModelIndex) -> int:
        return len(self._items)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._items):
            return None

        name, path = self._items[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return name
        if role == Qt.ItemDataRole.UserRole:
            return path
        if role == Qt.ItemDataRole.UserRole + 1:
            return Path(path).exists()
        return None

    def remove_item(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        self._items.pop(row)
        self.endRemoveRows()
        self._persist()

    def _persist(self):
        from pireal.gui.controller import Controller
        from pireal.registry import Registry

        controller = Registry.get("controller", Controller)
        # Reemplazar la lista entera en el controller
        paths = [path for _, path in self._items]
        controller.set_recent_databases(paths)


class RecentDBDelegate(QStyledItemDelegate):
    """
    Custom delegate that show database name and database path
    in same item
    """

    removeRequested = pyqtSignal(int)

    _PADDING = 8
    _BTN_SIZE = 20

    def paint(
        self,
        painter: QPainter | None,
        option: "QStyleOptionViewItem",
        index: QModelIndex,
    ) -> None:
        if painter is None:
            return

        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        opt.text = ""

        style = opt.widget.style() if opt.widget else QApplication.style()
        if style is None:
            return
        if opt.state & QStyle.StateFlag.State_Selected:
            highlight = opt.palette.color(QPalette.ColorRole.Highlight)
            highlight.setAlpha(150)
            opt.palette.setColor(QPalette.ColorRole.Highlight, highlight)
        style.drawControl(QStyle.ControlElement.CE_ItemViewItem, opt, painter, opt.widget)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        palette = opt.palette

        exits = index.data(Qt.ItemDataRole.UserRole + 1)
        is_selected = bool(opt.state & QStyle.StateFlag.State_Selected)

        if is_selected:
            text_color = palette.color(QPalette.ColorRole.HighlightedText)
        elif not exits:
            text_color = palette.color(QPalette.ColorRole.PlaceholderText)
        else:
            text_color = palette.color(QPalette.ColorRole.Text)

        if is_selected:
            sub_color = palette.color(QPalette.ColorRole.HighlightedText)
        else:
            sub_color = palette.color(QPalette.ColorRole.Text)
            sub_color.setAlpha(160)

        rect = option.rect.adjusted(self._PADDING, 0, -self._BTN_SIZE - self._PADDING, 0)
        half = rect.height() // 2

        name = index.data(Qt.ItemDataRole.DisplayRole) or ""
        path = index.data(Qt.ItemDataRole.UserRole) or ""

        name_font = painter.font()
        name_font.setBold(True)
        name_font.setPointSize(11)
        painter.setFont(name_font)
        painter.setPen(text_color)
        name_rect = QRect(rect.left(), rect.top(), rect.width(), half)
        painter.drawText(name_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, name)

        path_font = painter.font()
        path_font.setBold(False)
        path_font.setPointSize(9)
        painter.setFont(path_font)
        painter.setPen(sub_color)
        path_rect = QRect(rect.left(), rect.top() + half, rect.width(), half)
        metrics = painter.fontMetrics()
        elided = metrics.elidedText(path, Qt.TextElideMode.ElideLeft, path_rect.width())
        painter.drawText(
            path_rect,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            elided,
        )

        is_hover = bool(opt.state & QStyle.StateFlag.State_MouseOver)
        if is_hover or is_selected:
            btn_color = (
                palette.color(QPalette.ColorRole.HighlightedText)
                if is_selected
                else palette.color(QPalette.ColorRole.PlaceholderText)
            )
            painter.setPen(btn_color)
            btn_font = painter.font()
            btn_font.setPointSize(10)
            painter.setFont(btn_font)
            btn_rect = QRect(
                option.rect.right() - self._BTN_SIZE,
                option.rect.top(),
                self._BTN_SIZE,
                option.rect.height(),
            )
            painter.drawText(btn_rect, Qt.AlignmentFlag.AlignCenter, "✕")

        painter.restore()

    def editorEvent(self, event, model, option, index):
        from PyQt6.QtCore import QEvent

        if event.type() == QEvent.Type.MouseButtonRelease:
            btn_rect = QRect(
                option.rect.right() - self._BTN_SIZE,
                option.rect.top(),
                self._BTN_SIZE,
                option.rect.height(),
            )
            pos = event.position().toPoint() if hasattr(event, "position") else event.pos()
            if btn_rect.contains(pos):
                self.removeRequested.emit(index.row())
                return True
        return super().editorEvent(event, model, option, index)

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

        subtitle_rect = QRect(rect.left(), rect.top() + title_height, rect.width(), subtitle_height)

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
        size.setHeight(52)
        return size


class RecentDatabasesView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(4)

        label = QLabel(tr.TR_RECENT_DATABASES)
        font = label.font()
        font.setPointSize(font.pointSize() - 1)
        label.setFont(font)
        vbox.addWidget(label)

        self._empty_label = QLabel("No hay base de datos recientes.")
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        palette = self._empty_label.palette()
        self._empty_label.setStyleSheet(f"color: {palette.color(QPalette.ColorRole.PlaceholderText).name()};")
        vbox.addWidget(self._empty_label)

        self._recent_dbs_list = QListView()
        self._recent_dbs_list.setFrameShape(QListView.Shape.NoFrame)
        self._recent_dbs_list.setVerticalScrollMode(QListView.ScrollMode.ScrollPerPixel)
        self._recent_dbs_list.setSelectionMode(QListView.SelectionMode.SingleSelection)
        self._recent_dbs_list.setMinimumWidth(550)
        self._recent_dbs_list.setMouseTracking(True)
        vbox.addWidget(self._recent_dbs_list)

        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        model_data = []
        for recent_db in qsettings.value("recent_databases", type=list):
            name = os.path.splitext(os.path.basename(recent_db))[0]
            model_data.append((name, recent_db))

        self.model = RecentDBModel(model_data)
        self._recent_dbs_list.setModel(self.model)

        delegate = RecentDBDelegate()
        delegate.removeRequested.connect(self._on_remove)
        self._recent_dbs_list.setItemDelegate(delegate)

        self._update_empty_state()

    def _update_empty_state(self):
        has_items = self.model.rowCount() > 0
        self._empty_label.setVisible(not has_items)
        self._recent_dbs_list.setVisible(has_items)

    def _on_remove(self, row: int):
        self.model.remove_item(row)
        self._update_empty_state()


class StartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        palette = self.palette()
        highlight = palette.color(palette.ColorRole.Highlight).name()
        title_lbl = QLabel(f'<b><font color="{highlight}">π</font><span style="letter-spacing:2px;">real</span></b>')
        font = QFont("Monospace", 42, QFont.Weight.Bold)
        title_lbl.setFont(font)

        subtitle_lbl = QLabel("free and open source Relational Algebra Interpreter")
        font = subtitle_lbl.font()
        font.setPointSize(14)
        subtitle_lbl.setFont(font)

        # Buttons
        hbox_btn = QHBoxLayout()
        btn_open_db = QPushButton(tr.TR_OPEN_DB)
        btn_open_db.setMinimumSize(150, 0)
        btn_open_db.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        btn_new_db = QPushButton(tr.TR_NEW_DB)
        btn_new_db.setMinimumSize(150, 0)
        btn_new_db.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        btn_example = QPushButton(tr.TR_EXAMPLE_DB)
        btn_example.setMinimumSize(150, 0)
        btn_example.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        hbox_btn.addStretch()
        hbox_btn.addWidget(btn_open_db)
        hbox_btn.addWidget(btn_new_db)
        hbox_btn.addWidget(btn_example)
        hbox_btn.addStretch()

        # "or code your DB" link
        or_lbl = QLabel("or")
        or_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        or_font = or_lbl.font()
        or_font.setPointSize(9)
        or_lbl.setFont(or_font)
        or_lbl.setStyleSheet("color: #888;")

        code_link = QLabel(
            '<a href="code" style="text-decoration:none; color:#1565c0;">'
            "<tt>&lt;/&gt;</tt> code your database directly →"
            "</a>"
        )
        code_link.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        code_link.setCursor(Qt.CursorShape.PointingHandCursor)
        code_link.linkActivated.connect(lambda _: self._new_database_from_text())

        # List
        self._recent_databases_view = RecentDatabasesView()

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
        main_layout.addSpacing(16)
        main_layout.addLayout(hbox_btn)
        main_layout.addSpacing(4)
        main_layout.addWidget(or_lbl)
        main_layout.addWidget(code_link)
        main_layout.addSpacing(12)
        main_layout.addWidget(self._recent_databases_view, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.addStretch(1)
        if True:
            feedback_layout = QHBoxLayout()
            feedback_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            feedback_btn = QPushButton(tr.TR_FEEDBACK_BTN_SEND_START_PAGE)
            palette = feedback_btn.palette()
            normal_color = palette.color(palette.ColorRole.Link).name()
            feedback_btn.setStyleSheet(f"""
            QPushButton {{
                color: {normal_color};
                border: 1px solid {normal_color};
                border-radius: 4px;
                padding: 3px 10px;
            }}
            QPushButton:hover {{ background-color: rgba(0,0,0,0.05); }}
        """)
            feedback_btn.clicked.connect(self._send_feedback)

            feedback_layout.addWidget(feedback_btn)
            main_layout.addLayout(feedback_layout)

        main_layout.addLayout(hbox_footer)

        self._recent_databases_view._recent_dbs_list.doubleClicked.connect(self._on_listview_item_double_clicked)
        btn_open_db.clicked.connect(self._open_database)
        btn_new_db.clicked.connect(self._new_database)
        btn_example.clicked.connect(self._open_example)

    def _send_feedback(self):
        controller = Registry.get("controller", Controller)
        controller.send_feedback()

    def _new_database(self):
        controller = Registry.get("controller", Controller)
        controller.create_database()

    def _open_database(self, path: str):
        controller = Registry.get("controller", Controller)
        controller.open_database(path)

    def _open_example(self):
        controller = Registry.get("controller", Controller)
        controller.open_database(sample("database.pdb"))
        controller.open_query(sample("queries.pqf"))

        QTimer.singleShot(1300, controller.execute_queries)

    @Slot(QModelIndex)
    def _on_listview_item_double_clicked(self, index):
        path = self._recent_databases_view.model.data(index, role=Qt.ItemDataRole.UserRole)
        if path is not None:
            self._open_database(path)

    def _new_database_from_text(self):
        controller = Registry.get("controller", Controller)
        controller.create_database_from_text()
