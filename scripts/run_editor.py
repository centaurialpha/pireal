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

import sys

from PyQt6.QtWidgets import QApplication

from pireal.gui.editor import Editor
from pireal.gui.theme.manager import get_theme_manager
from pireal.settings import settings

app = QApplication(sys.argv)
settings.load()
get_theme_manager().apply(settings.theme)

editor = Editor()
editor.resize(800, 600)
editor.setPlainText("""
% Mostrar los nombres de los alumnos y su apoderado
q1 := alumno njoin apoderado;
q2 := project nombre, nombre_apoderado (q1);

% Mostrar el nombre de los alumnos inscriptos y el nombre de los cursos que tomaron
qq1 := alumno njoin (inscripto njoin curso);
qq2 := project nombre, nombre_curso (qq1);

% Mostrar los nombres y precios de los cursos con valor menor a 3000
query_1 := project nombre_curso, valor (select valor < 3000 (curso));

% Mostrar los nombres de los cursos que comienzan despues del mes de Marzo
query_11 := project nombre_curso, fecha_inicio (select fecha_inicio > '01/03/2017' (curso));

% Ejemplo de Left Outer Join
consulta_1 := alumno louter inscripto;
""")
editor.show()

sys.exit(app.exec())
