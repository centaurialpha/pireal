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

import textwrap

import pytest

from pireal.core.relation import Relation
from tests.helpers import evaluate


@pytest.mark.integration
def test_end_to_end_from_database_file(tmp_path):
    """
    Simula el flujo completo: leer un .pdb, cargar relaciones,
    ejecutar un conjunto de queries encadenadas y verificar resultados.
    """
    # 1. Simular un archivo .pdb
    db_content = textwrap.dedent("""\
    @estudiantes:id,nombre,edad,ciudad
    1,Gabriel,25,Córdoba
    2,Marisel,22,Buenos Aires
    3,Rodrigo,30,Córdoba
    4,Hector,19,Rosario

    @materias:id,nombre
    1,Base de Datos
    2,Algoritmos
    3,Redes

    @inscripciones:id,id_materia
    1,1
    1,2
    2,1
    3,3
    """)
    db_file = tmp_path / "test.pdb"
    db_file.write_text(db_content, encoding="utf-8")

    # 2. Leer y sanitizar como lo hace el controller
    from pireal.core.pireal_file import File
    from pireal.utils import sanitize_data

    file = File(str(db_file))
    data = sanitize_data(file.read())

    # 3. Construir relaciones como lo hace DatabaseContainer
    relations = {}
    for table in data["tables"]:
        r = Relation()
        r.header = table["header"]
        r.name = table["name"]
        for row in table["tuples"]:
            r.insert(row)
        relations[table["name"]] = r

    assert len(relations) == 3
    assert relations["estudiantes"].cardinality() == 4
    assert relations["materias"].cardinality() == 3

    # 4. Ejecutar queries encadenadas
    query = """\
    cordobeses := select ciudad='Córdoba' (estudiantes);
    jovenes_cordobeses := select edad < 30 (cordobeses);
    nombres := project nombre (jovenes_cordobeses);
    """
    results = evaluate(query, relations)

    assert "cordobeses" in results
    assert "jovenes_cordobeses" in results
    assert "nombres" in results

    assert results["cordobeses"].cardinality() == 2
    assert results["jovenes_cordobeses"].cardinality() == 1
    assert results["nombres"].header == ["nombre"]
    assert ("Gabriel",) in results["nombres"].content

    # 5. Join entre relaciones
    query_join = """\
    est_mat := inscripciones njoin estudiantes;
    """
    results_join = evaluate(query_join, relations)
    assert results_join["est_mat"].cardinality() == 4
    assert "nombre" in results_join["est_mat"].header
