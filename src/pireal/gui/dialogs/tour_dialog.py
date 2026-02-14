from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from pireal.dirs import DATA_SETTINGS

SLIDES = [
    {
        "icon": "🎓",
        "title": "Welcome to Pireal",
        "body": (
            "Pireal is a free and open source <b>Relational Algebra interpreter</b> "
            "designed for learning database fundamentals.<br><br>"
            "Perfect for students and teachers exploring how databases work under the hood."
        ),
    },
    {
        "icon": "🗄️",
        "title": "Create or open a Database",
        "body": (
            "You can open an existing <b>.pdb</b> file, create one step by step using the dialog, "
            "or go full nerd and <b>code your database directly</b> using the text syntax:<br><br>"
            "<tt>@students:id,name,age<br>"
            "1,Gabriel,25<br>"
            "2,Ana,22</tt>"
        ),
    },
    {
        "icon": "✏️",
        "title": "Write Relational Algebra queries",
        "body": (
            "Use the query editor to write <b>Relational Algebra expressions</b>:<br><br>"
            "<tt>adults := select age >= 18 (students);<br>"
            "names := project name (adults);</tt><br><br>"
            "Hit <b>▶</b> or use the run button to execute."
        ),
    },
    {
        "icon": "📊",
        "title": "Explore the results",
        "body": (
            "Every query result appears in the <b>Results panel</b> and the <b>sidebar</b>.<br><br>"
            "You can inspect each relation, see its cardinality and degree, "
            "and compare results side by side."
        ),
    },
]


class TourDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to Pireal")
        self.setMinimumSize(520, 340)
        self.resize(540, 360)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )

        self._current = 0
        self._build_ui()
        self._update_slide()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(32, 28, 32, 20)

        # Indicadores de progreso
        self._indicators_layout = QHBoxLayout()
        self._indicators_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._indicators = []
        for _ in SLIDES:
            dot = QLabel("●")
            dot.setStyleSheet("color: #ccc; font-size: 10px;")
            self._indicators.append(dot)
            self._indicators_layout.addWidget(dot)
        layout.addLayout(self._indicators_layout)

        # Ícono
        self._icon_lbl = QLabel()
        self._icon_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        font = self._icon_lbl.font()
        font.setPointSize(36)
        self._icon_lbl.setFont(font)
        layout.addWidget(self._icon_lbl)

        # Título
        self._title_lbl = QLabel()
        self._title_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        font = self._title_lbl.font()
        font.setPointSize(16)
        font.setBold(True)
        self._title_lbl.setFont(font)
        layout.addWidget(self._title_lbl)

        # Cuerpo
        self._body_lbl = QLabel()
        self._body_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._body_lbl.setWordWrap(True)
        self._body_lbl.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(self._body_lbl, stretch=1)

        # Botones
        btn_layout = QHBoxLayout()
        self._skip_btn = QPushButton("Skip tour")
        self._skip_btn.setFlat(True)
        self._skip_btn.clicked.connect(self._on_skip)

        self._next_btn = QPushButton("Next →")
        self._next_btn.setMinimumWidth(100)
        self._next_btn.clicked.connect(self._on_next)

        btn_layout.addWidget(self._skip_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self._next_btn)
        layout.addLayout(btn_layout)

    def _update_slide(self):
        slide = SLIDES[self._current]
        self._icon_lbl.setText(slide["icon"])
        self._title_lbl.setText(slide["title"])
        self._body_lbl.setText(slide["body"])

        # Actualizar indicadores
        for i, dot in enumerate(self._indicators):
            dot.setStyleSheet(
                "color: #1565c0; font-size: 10px;"
                if i == self._current
                else "color: #ccc; font-size: 10px;"
            )

        # Último slide: cambiar botón
        is_last = self._current == len(SLIDES) - 1
        self._next_btn.setText("Get started!" if is_last else "Next →")

    def _on_next(self):
        if self._current < len(SLIDES) - 1:
            self._current += 1
            self._update_slide()
        else:
            self._mark_seen()
            self.accept()

    def _on_skip(self):
        self._mark_seen()
        self.reject()

    def _mark_seen(self):
        qs = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        qs.setValue("tour_seen", True)

    @staticmethod
    def should_show() -> bool:
        qs = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        return not qs.value("tour_seen", False, type=bool)
