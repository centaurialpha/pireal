# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QFont
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
)

from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import EditorColorRole
from pireal.interpreter.tree_builder import NodeKind, TreeNode
from pireal.settings import settings


def _populate(
    parent: QTreeWidgetItem, node: TreeNode, scheme, base_font: QFont
) -> None:
    item = QTreeWidgetItem(parent, [node.label])
    editor = scheme.editor

    match node.kind:
        case NodeKind.ASSIGNMENT:
            font = QFont(base_font)
            font.setBold(True)
            item.setFont(0, font)
            item.setForeground(0, QBrush(editor.get(EditorColorRole.VARIABLE)))
        case NodeKind.UNARY_OP:
            font = QFont(base_font)
            font.setBold(True)
            item.setFont(0, font)
            item.setForeground(0, QBrush(editor.get(EditorColorRole.KEYWORD)))
        case NodeKind.BINARY_OP:
            font = QFont(base_font)
            font.setBold(True)
            item.setFont(0, font)
            item.setForeground(0, QBrush(editor.get(EditorColorRole.OPERATOR)))
        case NodeKind.CONDITION:
            font = QFont(base_font)
            font.setItalic(True)
            item.setFont(0, font)
            item.setForeground(0, QBrush(editor.get(EditorColorRole.STRING)))
        case NodeKind.RELATION:
            item.setForeground(0, QBrush(editor.get(EditorColorRole.NUMBER)))

    # if node.tooltip:
    #     item.setToolTip(0, node.tooltip)

    for child in node.children:
        _populate(item, child, scheme, base_font)


class TreeDialog(QDialog):
    def __init__(self, roots: list[TreeNode], parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowTitle("Execution Tree")
        self.resize(500, 500)

        self._roots = roots

        layout = QVBoxLayout(self)

        self._tree = QTreeWidget()
        self._tree.setHeaderHidden(True)
        self._tree.setFont(QFont(settings.font_family, settings.font_size))

        scheme = get_theme_manager().current_scheme
        pal = self._tree.palette()
        pal.setColor(pal.ColorRole.Base, scheme.editor.background)
        pal.setColor(pal.ColorRole.Text, scheme.editor.foreground)
        self._tree.setPalette(pal)

        base_font = QFont(settings.font_family, settings.font_size)
        for root in roots:
            _populate(self._tree.invisibleRootItem(), root, scheme, base_font)

        self._tree.expandAll()
        layout.addWidget(self._tree)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        settings.settingsChanged.connect(self._on_settings_changed)
        get_theme_manager().themeChanged.connect(self._on_theme_changed)

    def _on_settings_changed(self, key: str):
        if key in ("font_family", "font_size"):
            self._tree.setFont(QFont(settings.font_family, settings.font_size))

    def _on_theme_changed(self, scheme):
        pal = self._tree.palette()
        pal.setColor(pal.ColorRole.Base, scheme.editor.background)
        pal.setColor(pal.ColorRole.Text, scheme.editor.foreground)
        self._tree.setPalette(pal)
        self._tree.clear()
        base_font = QFont(settings.font_family, settings.font_size)
        for root in self._roots:
            _populate(self._tree.invisibleRootItem(), root, scheme, base_font)

        self._tree.expandAll()
