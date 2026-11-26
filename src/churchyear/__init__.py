"""The church year for Lutheran (ELCA) congregations.

    >>> import datetime as dt, churchyear
    >>> day = churchyear.church_day(dt.date(2026, 12, 6))
    >>> day.name, day.rcl_year, day.color
    ('Second Sunday of Advent', 'B', 'blue')
"""

from .commemorations import Commemoration, all_commemorations, commemorations_on
from .core import (
    HOLIDAYS,
    SEASONS,
    advent_start,
    easter,
    holiday_date,
    next_sunday,
    patriotic_holiday,
    season,
)
from .lectionary import (
    COLORS,
    LITURGICAL_SEASONS,
    ChurchDay,
    church_day,
    church_year_start,
    color,
    day_name,
    lectionary_number,
    liturgical_season,
    rcl_year,
)

__version__ = "1.0.0"

__all__ = [
    "COLORS",
    "HOLIDAYS",
    "LITURGICAL_SEASONS",
    "SEASONS",
    "ChurchDay",
    "Commemoration",
    "advent_start",
    "all_commemorations",
    "church_day",
    "church_year_start",
    "color",
    "commemorations_on",
    "day_name",
    "easter",
    "holiday_date",
    "lectionary_number",
    "liturgical_season",
    "next_sunday",
    "patriotic_holiday",
    "rcl_year",
    "season",
]
