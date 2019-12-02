import datetime
import pytest

from pireal.core.rtypes import RelationStr


@pytest.mark.parametrize(
    'value, expected',
    [
        ('1234', 1234),
        ('-1234', -1234),
        ('0', 0)
    ]
)
def test_int(value, expected):
    assert RelationStr(value).cast() == expected


@pytest.mark.parametrize(
    'value, expected',
    [
        ('3.1415', 3.1415),
        ('-3.1415', -3.1415),
        ('0.0', 0.0)
    ]
)
def test_float(value, expected):
    float_value = RelationStr(value).cast()
    assert isinstance(float_value, float)
    assert float_value == expected


@pytest.mark.parametrize(
    'value, hours, minutes',
    [
        ('13:15', 13, 15),
        ('00:00', 0, 0)
    ]
)
def test_time(value, hours, minutes):
    time_value = RelationStr(value).cast()
    assert isinstance(time_value, datetime.time)
    assert time_value.hour == hours
    assert time_value.minute == minutes


@pytest.mark.parametrize(
    'value, day, month, year',
    [
        ('1991/01/20', 20, 1, 1991),
        ('20/01/1991', 20, 1, 1991)
    ]
)
def test_date(value, day, month, year):
    date_value = RelationStr(value).cast()
    assert isinstance(date_value, datetime.date)
    assert date_value.day == day
    assert date_value.month == month
    assert date_value.year == year


def test_date_with_syntax_error():
    with pytest.raises(SyntaxError):
        RelationStr('01/20/1991').cast()
