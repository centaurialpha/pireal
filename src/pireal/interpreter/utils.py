from __future__ import annotations

import datetime


def is_date(string) -> tuple[bool, datetime.date | None]:
    ok = True
    date = None
    try:
        date = datetime.datetime.strptime(string, "%d/%m/%Y").date()
    except ValueError:
        try:
            date = datetime.datetime.strptime(string, "%Y/%m/%d").date()
        except ValueError:
            ok = False

    return ok, date


def is_time(string) -> tuple[bool, datetime.time | None]:
    ok = True
    time = None
    try:
        time = datetime.datetime.strptime(string, "%H:%M").time()
    except ValueError:
        ok = False
    return ok, time
