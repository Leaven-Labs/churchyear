# churchyear

The church year for Lutheran (ELCA) congregations, as a small Python package with no
dependencies: seasons, named Sundays and festivals, liturgical colors, the Revised Common
Lectionary year (A, B or C) and lectionary numbers, and the calendar of lesser festivals and
commemorations.

Part of [Leaven Labs](https://www.leavenlabs.org). Used by
[ChurchRadio Studio](https://github.com/Leaven-Labs/ChurchRadio-Studio) and ChurchRadio Manager.
MIT licensed.

```python
import datetime as dt
import churchyear

day = churchyear.church_day(dt.date(2026, 12, 6))
day.name          # 'Second Sunday of Advent'
day.season_name   # 'Advent'
day.color         # 'blue'
day.rcl_year      # 'B'  (Advent 1, 2026 begins Year B)

churchyear.day_name(dt.date(2027, 6, 6))           # 'Third Sunday after Pentecost'
churchyear.lectionary_number(dt.date(2027, 6, 6))  # 10
churchyear.easter(2027)                            # datetime.date(2027, 3, 28)
```

## What's in it

| Function | Gives |
|---|---|
| `church_day(date)` | Everything below for one date, as a `ChurchDay` |
| `day_name(date)` | The name of a Sunday, principal festival or day of Holy Week, else `None` |
| `liturgical_season(date)` | `advent`, `christmas`, `time_after_epiphany`, `lent`, `three_days`, `easter` or `time_after_pentecost` |
| `color(date)` | The day's color (ELW's first choice where it gives two) |
| `rcl_year(date)` | `"A"`, `"B"` or `"C"` |
| `lectionary_number(date)` | Lectionary 8 to 34 on Sundays after Holy Trinity |
| `commemorations_on(date)` | Lesser festivals and commemorations on that date (checked ones only; see below) |
| `easter(year)`, `advent_start(year)` | The two dates everything else hangs on |
| `season(date)` | ChurchRadio Studio's song seasons (`advent` … `holyweek` … `pentecost`), unchanged from Studio |
| `patriotic_holiday(date)`, `holiday_date(name, year)` | Civil holiday weekends (Memorial Day, July 4, Veterans Day, Labor Day) |

Names and colors follow *Evangelical Lutheran Worship* (2006). The package holds only names and
dates, which are facts; it never includes ELW's texts.

## The commemorations list needs checking

`src/churchyear/data/commemorations.csv` lists the lesser festivals and commemorations by date.
It was put together from public sources (mainly Wikipedia's "Calendar of saints (Lutheran)",
which mixes the ELW and LSB calendars) and **hasn't yet been checked against the calendar printed
in ELW**. Every row says `checked=no` until someone has compared it with ELW and changed it to
`yes`. `commemorations_on()` and `church_day()` return only checked rows, so nothing unchecked
reaches a broadcast or a bulletin by accident (`include_unchecked=True` shows the rest).

## For developers

Python 3.11 or later.

```
uv sync
uv run pytest
uv run ruff check . && uv run ruff format .
```

Without uv: `python -m pytest` from this folder works too (the tests find `src/` themselves).
