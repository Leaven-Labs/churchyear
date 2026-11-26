"""Easter, Advent, the seasons and civil holidays.

Moved from ChurchRadio Studio's churchyear.py with its behavior unchanged: Studio's songs are
tagged with these season names, so `season()` must keep giving the same answers.
"""

import datetime as dt

# Studio's song seasons. Holy Week has its own name here (songs for Palm Sunday through Holy
# Saturday); for the church's own seasons see `liturgical_season()`.
SEASONS = ["advent", "christmas", "epiphany", "lent", "holyweek", "easter", "pentecost"]

# Civil holidays whose weekend Studio marks (patriotic songs play only then).
HOLIDAYS = ["memorial", "independence", "veterans"]


def easter(year: int) -> dt.date:
    """Western Easter Sunday (Anonymous Gregorian algorithm)."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7  # noqa: E741 (the algorithm's own name)
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return dt.date(year, month, day + 1)


def advent_start(year: int) -> dt.date:
    """First Sunday of Advent: the fourth Sunday before Christmas Day."""
    xmas = dt.date(year, 12, 25)
    days_back = (xmas.weekday() + 1) % 7 or 7  # last Sunday before Dec 25
    return xmas - dt.timedelta(days=days_back + 21)


def season(date: dt.date) -> str:
    """Return the season name for a date (one of SEASONS)."""
    y = date.year
    if date >= advent_start(y) and date < dt.date(y, 12, 25):
        return "advent"
    if date >= dt.date(y, 12, 25) or date <= dt.date(y, 1, 5):
        return "christmas"
    e = easter(y)
    ash_wed = e - dt.timedelta(days=46)
    palm_sun = e - dt.timedelta(days=7)
    pentecost_day = e + dt.timedelta(days=49)
    if date < ash_wed:
        return "epiphany"
    if date < palm_sun:
        return "lent"
    if date < e:
        return "holyweek"
    if date < pentecost_day:
        return "easter"
    return "pentecost"  # Pentecost Day and the time after Pentecost


def holiday_date(name: str, year: int) -> dt.date:
    """Date of a civil holiday: memorial, independence, veterans or labor."""
    if name == "memorial":  # last Monday in May
        d = dt.date(year, 5, 31)
        return d - dt.timedelta(days=d.weekday())
    if name == "independence":
        return dt.date(year, 7, 4)
    if name == "veterans":
        return dt.date(year, 11, 11)
    if name == "labor":  # first Monday in September
        d = dt.date(year, 9, 1)
        return d + dt.timedelta(days=(7 - d.weekday()) % 7)
    raise ValueError(f"Unknown holiday: {name}")


def patriotic_holiday(date: dt.date, holidays=HOLIDAYS) -> str | None:
    """Name of the civil holiday whose weekend this date is in, else None.
    The weekend is the Sunday nearest the holiday (3 days before to 3 days after)."""
    wd = date.weekday()  # Mon=0 .. Sun=6; Mon-Wed belong to the Sunday before
    sunday = date - dt.timedelta(days=wd + 1) if wd < 3 else date + dt.timedelta(days=6 - wd)
    for name in holidays:
        if abs((holiday_date(name, sunday.year) - sunday).days) <= 3:
            return name
    return None


def next_sunday(today: dt.date) -> dt.date:
    """The coming Sunday, or today when today is a Sunday."""
    return today + dt.timedelta(days=(6 - today.weekday()) % 7)
