from datetime import datetime


def is_date(string) -> bool:
    ok = True
    try:
        datetime.strptime(string, '%d/%m/%Y')
    except ValueError:
        try:
            datetime.strptime(string, '%Y/%m/%d')
        except ValueError:
            ok = False
    return ok


def is_time(string) -> bool:
    ok = True
    try:
        datetime.strptime(string, '%H:%M')
    except ValueError:
        ok = False
    return ok
