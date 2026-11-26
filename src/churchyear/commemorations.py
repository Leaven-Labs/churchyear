"""Lesser festivals and commemorations on fixed dates (names and dates only).

The list is in data/commemorations.csv. Each row says whether someone has checked it against
the ELW calendar (`checked`). Anything that goes on air or into print should use only checked
rows: `commemorations_on(date)` returns only those unless asked for all.
"""

import csv
import datetime as dt
import io
from dataclasses import dataclass
from functools import cache
from importlib import resources

RANKS = ("lesser festival", "commemoration")


@dataclass(frozen=True)
class Commemoration:
    month: int
    day: int
    name: str
    rank: str  # "lesser festival" or "commemoration"
    checked: bool  # checked against the ELW calendar by a person


@cache
def all_commemorations() -> tuple[Commemoration, ...]:
    """Every row of the data file, in date order."""
    text = resources.files("churchyear").joinpath("data", "commemorations.csv").read_text(
        encoding="utf-8"
    )
    rows = []
    for row in csv.DictReader(io.StringIO(text)):
        if row["rank"] not in RANKS:
            raise ValueError(f"Unknown rank {row['rank']!r} for {row['name']!r}")
        if row["checked"] not in ("yes", "no"):
            raise ValueError(f"checked must be yes or no for {row['name']!r}")
        rows.append(
            Commemoration(
                month=int(row["month"]),
                day=int(row["day"]),
                name=row["name"],
                rank=row["rank"],
                checked=row["checked"] == "yes",
            )
        )
    return tuple(sorted(rows, key=lambda c: (c.month, c.day)))


def commemorations_on(date: dt.date, include_unchecked: bool = False) -> list[Commemoration]:
    """Lesser festivals and commemorations on this date. Only rows checked against ELW unless
    include_unchecked is True."""
    return [
        c
        for c in all_commemorations()
        if (c.month, c.day) == (date.month, date.day) and (c.checked or include_unchecked)
    ]
