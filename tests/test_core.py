"""ChurchRadio Studio's church-year tests, unchanged, plus more known dates."""

import datetime as dt

import pytest

import churchyear as cy

D = dt.date


# ---- From ChurchRadio Studio (tests/test_core.py, class ChurchYear) ---------------------------


def test_easter():
    assert cy.easter(2026) == D(2026, 4, 5)
    assert cy.easter(2027) == D(2027, 3, 28)
    assert cy.easter(2025) == D(2025, 4, 20)


def test_advent_start():
    assert cy.advent_start(2026) == D(2026, 11, 29)
    assert cy.advent_start(2027) == D(2027, 11, 28)
    assert cy.advent_start(2022) == D(2022, 11, 27)  # Christmas on Sunday


@pytest.mark.parametrize(
    ("date", "want"),
    [
        (D(2026, 11, 22), "pentecost"),
        (D(2026, 11, 29), "advent"),
        (D(2026, 12, 24), "advent"),
        (D(2026, 12, 25), "christmas"),
        (D(2027, 1, 5), "christmas"),
        (D(2027, 1, 6), "epiphany"),
        (D(2027, 2, 9), "epiphany"),
        (D(2027, 2, 10), "lent"),
        (D(2027, 3, 21), "holyweek"),
        (D(2027, 3, 28), "easter"),
        (D(2027, 5, 16), "pentecost"),
        (D(2026, 10, 11), "pentecost"),
    ],
)
def test_seasons(date, want):
    assert cy.season(date) == want


def test_patriotic_weekends():
    yes = {
        D(2026, 5, 24): "memorial",
        D(2026, 5, 25): "memorial",  # Memorial Day is 5/25
        D(2026, 7, 5): "independence",  # July 4 is a Saturday
        D(2026, 11, 8): "veterans",  # 11/11 is a Wednesday
        D(2027, 11, 14): "veterans",  # 11/11 is a Thursday
    }
    for date, want in yes.items():
        assert cy.patriotic_holiday(date) == want, date
    for date in (D(2026, 5, 17), D(2026, 5, 31), D(2026, 11, 15), D(2026, 10, 11)):
        assert cy.patriotic_holiday(date) is None, date
    assert cy.patriotic_holiday(D(2026, 9, 6)) is None
    assert cy.patriotic_holiday(D(2026, 9, 6), ["labor"]) == "labor"


# ---- More known dates -----------------------------------------------------------------------

# Western Easter, checked against published tables.
EASTERS = {
    1818: D(1818, 3, 22),  # earliest possible
    1943: D(1943, 4, 25),  # latest possible
    2000: D(2000, 4, 23),
    2008: D(2008, 3, 23),
    2011: D(2011, 4, 24),
    2016: D(2016, 3, 27),
    2019: D(2019, 4, 21),
    2024: D(2024, 3, 31),
    2028: D(2028, 4, 16),
    2029: D(2029, 4, 1),
    2030: D(2030, 4, 21),
    2038: D(2038, 4, 25),
    2285: D(2285, 3, 22),
}


@pytest.mark.parametrize(("year", "want"), EASTERS.items())
def test_easter_known_dates(year, want):
    assert cy.easter(year) == want


def test_easter_is_always_a_sunday_in_range():
    for year in range(1900, 2200):
        e = cy.easter(year)
        assert e.weekday() == 6
        assert D(year, 3, 22) <= e <= D(year, 4, 25)


def test_advent_start_is_a_sunday_between_nov_27_and_dec_3():
    for year in range(1900, 2200):
        a = cy.advent_start(year)
        assert a.weekday() == 6
        assert D(year, 11, 27) <= a <= D(year, 12, 3)


def test_season_edges_2027():
    # Easter 2027 is March 28.
    assert cy.season(D(2027, 3, 20)) == "lent"  # Saturday before Palm Sunday
    assert cy.season(D(2027, 3, 27)) == "holyweek"  # Holy Saturday
    assert cy.season(D(2027, 5, 15)) == "easter"  # day before Pentecost
    assert cy.season(D(2027, 11, 27)) == "pentecost"  # day before Advent 1
    assert cy.season(D(2027, 11, 28)) == "advent"


def test_labor_day_and_unknown_holiday():
    assert cy.holiday_date("labor", 2026) == D(2026, 9, 7)
    with pytest.raises(ValueError):
        cy.holiday_date("arbor", 2026)


def test_next_sunday():
    assert cy.next_sunday(D(2026, 11, 26)) == D(2026, 11, 29)  # Thursday
    assert cy.next_sunday(D(2026, 11, 29)) == D(2026, 11, 29)  # a Sunday is its own
