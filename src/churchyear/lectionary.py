"""Named days, the church's seasons and colors, and the Revised Common Lectionary year.

Names, colors and season boundaries follow Evangelical Lutheran Worship (ELW, 2006) as used in
the ELCA. Only names and dates are here (facts), never ELW's texts.
"""

import datetime as dt
from dataclasses import dataclass, field

from .commemorations import Commemoration, commemorations_on
from .core import advent_start, easter

_DAY = dt.timedelta(days=1)
_WEEK = dt.timedelta(days=7)

# The church's own seasons (ELW). Studio's simpler song seasons are `churchyear.season()`.
LITURGICAL_SEASONS = {
    "advent": "Advent",
    "christmas": "Christmas",
    "time_after_epiphany": "Time after Epiphany",
    "lent": "Lent",
    "three_days": "The Three Days",
    "easter": "Easter",
    "time_after_pentecost": "Time after Pentecost",
}

COLORS = ["blue", "white", "green", "purple", "scarlet", "red", "black", "none"]

_ORDINALS = [
    "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth",
    "Tenth", "Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Fifteenth", "Sixteenth",
    "Seventeenth", "Eighteenth", "Nineteenth", "Twentieth", "Twenty-first", "Twenty-second",
    "Twenty-third", "Twenty-fourth", "Twenty-fifth", "Twenty-sixth", "Twenty-seventh",
    "Twenty-eighth", "Twenty-ninth",
]  # fmt: skip


def _ordinal(n: int) -> str:
    return _ORDINALS[n - 1]


def church_year_start(date: dt.date) -> dt.date:
    """First Sunday of Advent of the church year that contains this date."""
    start = advent_start(date.year)
    return start if date >= start else advent_start(date.year - 1)


def rcl_year(date: dt.date) -> str:
    """Revised Common Lectionary year, "A", "B" or "C". A new year starts on Advent 1:
    Advent 2025 began Year A, Advent 2026 begins Year B."""
    ends_in = church_year_start(date).year + 1  # the calendar year most of it falls in
    return {1: "A", 2: "B", 0: "C"}[ends_in % 3]


def _key_dates(year: int) -> dict[str, dt.date]:
    e = easter(year)
    return {
        "ash_wednesday": e - 46 * _DAY,
        "palm_sunday": e - _WEEK,
        "easter": e,
        "ascension": e + 39 * _DAY,
        "pentecost": e + 49 * _DAY,
        "holy_trinity": e + 56 * _DAY,
        "advent": advent_start(year),
        "christ_the_king": advent_start(year) - _WEEK,
    }


def liturgical_season(date: dt.date) -> str:
    """The church's season (a key of LITURGICAL_SEASONS). Christmas runs Dec 25 to Jan 5;
    Lent runs from Ash Wednesday to the Wednesday of Holy Week; the Three Days are Maundy
    Thursday to Holy Saturday; Easter runs from Easter Day to the Day of Pentecost."""
    y = date.year
    k = _key_dates(y)
    if k["advent"] <= date < dt.date(y, 12, 25):
        return "advent"
    if date >= dt.date(y, 12, 25) or date <= dt.date(y, 1, 5):
        return "christmas"
    if date < k["ash_wednesday"]:
        return "time_after_epiphany"
    if date < k["easter"] - 3 * _DAY:
        return "lent"
    if date < k["easter"]:
        return "three_days"
    if date <= k["pentecost"]:
        return "easter"
    return "time_after_pentecost"


def lectionary_number(date: dt.date) -> int | None:
    """ELW's lectionary number for a Sunday after Holy Trinity (Lectionary 8 to 34, the RCL's
    Proper 3 to 29), else None. Lectionary 8 is the Sunday between May 24 and 28; each one after
    that covers a week starting May 29 (Lectionary 9), so Christ the King is Lectionary 34."""
    if date.weekday() != 6:
        return None
    k = _key_dates(date.year)
    if not k["holy_trinity"] < date < k["advent"]:
        return None
    if dt.date(date.year, 5, 24) <= date <= dt.date(date.year, 5, 28):
        return 8
    return 9 + (date - dt.date(date.year, 5, 29)).days // 7


def _named_day(date: dt.date) -> tuple[str, str] | None:
    """(name, color) of a Sunday, principal festival or Holy Week day, else None."""
    y, m, d = date.year, date.month, date.day
    k = _key_dates(y)
    sunday = date.weekday() == 6

    # Advent. When Dec 24 is a Sunday it is the Fourth Sunday of Advent (Christmas Eve is
    # that evening).
    if sunday and k["advent"] <= date < dt.date(y, 12, 25):
        n = (date - k["advent"]).days // 7 + 1
        return f"{_ordinal(n)} Sunday of Advent", "blue"

    # Fixed festivals of Christmas and Epiphany.
    if (m, d) == (12, 24):
        return "Nativity of Our Lord / Christmas Eve", "white"
    if (m, d) == (12, 25):
        return "Nativity of Our Lord / Christmas Day", "white"
    if (m, d) == (1, 6):
        return "Epiphany of Our Lord", "white"

    if sunday and (date >= dt.date(y, 12, 26) or date == dt.date(y, 1, 1)):
        return "First Sunday of Christmas", "white"
    if sunday and dt.date(y, 1, 2) <= date <= dt.date(y, 1, 5):
        return "Second Sunday of Christmas", "white"

    # Time after Epiphany: Baptism of Our Lord is the Sunday Jan 7-13; Transfiguration is the
    # Sunday before Ash Wednesday.
    if sunday and dt.date(y, 1, 7) <= date < k["ash_wednesday"]:
        if date == k["ash_wednesday"] - 3 * _DAY:
            return "Transfiguration of Our Lord", "white"
        if date <= dt.date(y, 1, 13):
            return "Baptism of Our Lord", "white"
        baptism = date - ((date - dt.date(y, 1, 7)).days // 7) * _WEEK
        n = (date - baptism).days // 7 + 1
        return f"{_ordinal(n)} Sunday after Epiphany", "green"

    # Lent and Holy Week.
    if date == k["ash_wednesday"]:
        return "Ash Wednesday", "purple"
    if sunday and k["ash_wednesday"] < date < k["palm_sunday"]:
        n = (date - k["ash_wednesday"]).days // 7 + 1
        return f"{_ordinal(n)} Sunday in Lent", "purple"
    holy_week = {
        0: ("Sunday of the Passion / Palm Sunday", "scarlet"),
        1: ("Monday in Holy Week", "scarlet"),
        2: ("Tuesday in Holy Week", "scarlet"),
        3: ("Wednesday in Holy Week", "scarlet"),
        4: ("Maundy Thursday", "scarlet"),
        5: ("Good Friday", "none"),
        6: ("Resurrection of Our Lord / Vigil of Easter", "white"),
    }
    if k["palm_sunday"] <= date < k["easter"]:
        return holy_week[(date - k["palm_sunday"]).days]

    # Easter to the end of the church year.
    if date == k["easter"]:
        return "Resurrection of Our Lord / Easter Day", "white"
    if sunday and k["easter"] < date < k["pentecost"]:
        n = (date - k["easter"]).days // 7 + 1
        return f"{_ordinal(n)} Sunday of Easter", "white"
    if date == k["ascension"]:
        return "Ascension of Our Lord", "white"
    if date == k["pentecost"]:
        return "Day of Pentecost", "red"
    if date == k["holy_trinity"]:
        return "The Holy Trinity", "white"
    if date == k["christ_the_king"]:
        return "Christ the King", "white"
    if sunday and k["holy_trinity"] < date < k["advent"]:
        n = (date - k["pentecost"]).days // 7
        return f"{_ordinal(n)} Sunday after Pentecost", "green"
    return None


_SEASON_COLORS = {
    "advent": "blue",
    "christmas": "white",
    "time_after_epiphany": "green",
    "lent": "purple",
    "three_days": "scarlet",
    "easter": "white",
    "time_after_pentecost": "green",
}


def day_name(date: dt.date) -> str | None:
    """Name of a Sunday, principal festival or day of Holy Week, else None (an ordinary
    weekday; see `commemorations_on()` for lesser festivals and commemorations)."""
    named = _named_day(date)
    return named[0] if named else None


def color(date: dt.date) -> str:
    """ELW's color for the day (its first choice where ELW gives two)."""
    named = _named_day(date)
    if named:
        return named[1]
    return _SEASON_COLORS[liturgical_season(date)]


@dataclass(frozen=True)
class ChurchDay:
    """Everything about one date in the church year."""

    date: dt.date
    name: str | None  # Sunday, principal festival or Holy Week day; None on ordinary weekdays
    season: str  # a key of LITURGICAL_SEASONS
    season_name: str  # e.g. "Time after Pentecost"
    color: str
    rcl_year: str  # "A", "B" or "C"
    lectionary: int | None  # Lectionary 8-34 on Sundays after Holy Trinity
    sunday: dt.date  # this date if a Sunday, else the Sunday before it
    sunday_name: str | None  # the name of that Sunday
    commemorations: list[Commemoration] = field(default_factory=list)


def church_day(date: dt.date) -> ChurchDay:
    """Everything about one date: its name, season, color, lectionary year and number, the
    Sunday it belongs to and the lesser festivals and commemorations on it."""
    sunday = date - dt.timedelta(days=(date.weekday() + 1) % 7)
    s = liturgical_season(date)
    return ChurchDay(
        date=date,
        name=day_name(date),
        season=s,
        season_name=LITURGICAL_SEASONS[s],
        color=color(date),
        rcl_year=rcl_year(date),
        lectionary=lectionary_number(date),
        sunday=sunday,
        sunday_name=day_name(sunday),
        commemorations=commemorations_on(date),
    )
