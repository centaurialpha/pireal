import pytest
import unittest
from collections import OrderedDict

from pireal.core import file_manager
from pireal.core import relation


@pytest.mark.parametrize(
    'filename, expected',
    [
        ('/home/gabo/archivo.py', '.py'),
        ('/path/path/blabla/file.extension', '.extension'),
        ('/hola/como/estas/que_onda.qda', '.qda')
    ]
)
def test_get_extension(filename, expected):
    assert file_manager.get_extension(filename) == expected


@pytest.mark.parametrize(
    'filename, name',
    [
        ('/home/gabo/archivo.py', 'archivo'),
        ('/path/path/blabla/file.extension', 'file'),
        ('/hola/como/estas/que_onda.qda', 'que_onda')
    ]
)
def test_get_basename(filename, name):
    assert file_manager.get_basename(filename) == name


@pytest.mark.parametrize(
    'filename, name',
    [
        ('/home/gabo/archivo.py', 'archivo.py'),
        ('/path/path/blabla/file.extension', 'file.extension'),
        ('/hola/como/estas/que_onda.qda', 'que_onda.qda')
    ]
)
def test_get_basename_with_extension(filename, name):
    assert file_manager.get_basename_with_extension(filename) == name


@pytest.mark.parametrize(
    'filename, path',
    [
        ('/home/gabo/archivo.py', '/home/gabo'),
        ('/path/path/blabla/file.extension', '/path/path/blabla'),
        ('/hola/como/estas/que_onda.qda', '/hola/como/estas')
    ]
)
def test_get_path(filename, path):
    assert file_manager.get_path(filename) == path


def test_get_files_from_folder(tmpdir):
    files = (
        'archivo.py',
        'archivo2.py',
        'archivo3.py'
    )
    assert len(tmpdir.listdir()) == 0
    for f in files:
        path = tmpdir.join(f)
        # print(path)
        path.write("Some content")
    assert len(tmpdir.listdir()) == len(files)
    _files = file_manager.get_files_from_folder(tmpdir.strpath)
    assert len(_files) == len(files)


def test_generate_database():
    # XXX: acerca de este test
    # lo ideal seria assertear el resultado con lo esperado pero
    # no como tupla sino como un string.
    # La implementación actual de Relation.content es un set
    # (para aprovechar las operaciones sobre conjuntos),
    # por lo tanto no importa el órden. Considerar mejorar eso

    r1 = relation.Relation()
    r1.header = ['id', 'name']
    r1.content.add(('1', 'gabox'))
    r1.content.add(('23', 'rodrigo'))

    r2 = relation.Relation()
    r2.header = ['id', 'skill']
    r2.content = {('23', 'games')}

    relations = OrderedDict()
    relations['people'] = r1
    relations['skills'] = r2
    expected = (
        '@people:id,name',
        '1,gabox',
        '23,rodrigo',
        '@skills:id,skill',
        '23,games'
    )
    result = file_manager.generate_database(relations)
    for expec in expected:
        assert expec in result


def test_database_text_content_simple_content():
    text = '@persona:name,age\ngabo,28\nmechi,25'
    expected = [{
        'name': 'persona',
        'header': ['name', 'age'],
        'tuples': [('gabo', '28'), ('mechi', '25')]
    }]
    result = file_manager.parse_database_content(text)
    assert result == expected


def test_database_text_content_with_two_relations():
    text = """
    @persona:name,age\ngabo,28\nrodrigo,20\n
    @skills:name,skill\nrodrigo,games\ngabo,python"""
    expected = [{
        'name': 'persona',
        'header': ['name', 'age'],
        'tuples': [('gabo', '28'), ('rodrigo', '20')]
    }, {
        'name': 'skills',
        'header': ['name', 'skill'],
        'tuples': [('rodrigo', 'games'), ('gabo', 'python')]
    }]
    result = file_manager.parse_database_content(text)
    assert result == expected


def test_clean_parse_database_text_content():
    text = '@persona:name,age\ngabo,28\nmechi,25\r'
    expected = [{
        'name': 'persona',
        'header': ['name', 'age'],
        'tuples': [('gabo', '28'), ('mechi', '25')]
    }]
    result = file_manager.parse_database_content(text)
    assert result == expected


def test_database_text_content_simple_content_ignore_lasts():
    text = '@persona:name,age\ngabo,28,ignore\nmechi,25,ignore2,ignore3'
    expected = [{
        'name': 'persona',
        'header': ['name', 'age'],
        'tuples':  [('gabo', '28'), ('mechi', '25')]
    }]
    result = file_manager.parse_database_content(text)
    assert result == expected
