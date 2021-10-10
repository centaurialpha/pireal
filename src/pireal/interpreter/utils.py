from datetime import datetime


def is_date(string) -> bool:
    ok = True
    date = None
    try:
        date = datetime.strptime(string, '%d/%m/%Y').date()
    except ValueError:
        try:
            date = datetime.strptime(string, '%Y/%m/%d').date()
        except ValueError:
            ok = False
    return ok, date


def is_time(string) -> bool:
    ok = True
    time = None
    try:
        time = datetime.strptime(string, '%H:%M').time()
    except ValueError:
        ok = False
    return ok, time
