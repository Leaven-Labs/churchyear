"""Named days, seasons, colors and lectionary years, checked against known dates."""

import datetime as dt

import pytest

import churchyear as cy

D = dt.date

# The church year 2026-27 (Year B): Advent 1 is Nov 29, 2026; Easter is March 28, 2027.
NAMED_2026_27 = {
    D(2026, 11, 29): ("First Sunday of Advent", "blue"),
    D(2026, 12, 6): ("Second Sunday of Advent", "blue"),
    D(2026, 12, 20): ("Fourth Sunday of Advent", "blue"),
    D(2026, 12, 24): ("Nativity of Our Lord / Christmas Eve", "white"),
    D(2026, 12, 25): ("Nativity of Our Lord / Christmas Day", "white"),
    D(2026, 12, 27): ("First Sunday of Christmas", "white"),
    D(2027, 1, 3): ("Second Sunday of Christmas", "white"),
    D(2027, 1, 6): ("Epiphany of Our Lord", "white"),
    D(2027, 1, 10): ("Baptism of Our Lord", "white"),
    D(2027, 1, 17): ("Second Sunday after Epiphany", "green"),
    D(2027, 1, 31): ("Fourth Sunday after Epiphany", "green"),
    D(2027, 2, 7): ("Transfiguration of Our Lord", "white"),
    D(2027, 2, 10): ("Ash Wednesday", "purple"),
    D(2027, 2, 14): ("First Sunday in Lent", "purple"),
    D(2027, 3, 14): ("Fifth Sunday in Lent", "purple"),
    D(2027, 3, 21): ("Sunday of the Passion / Palm Sunday", "scarlet"),
    D(2027, 3, 24): ("Wednesday in Holy Week", "scarlet"),
    D(2027, 3, 25): ("Maundy Thursday", "scarlet"),
    D(2027, 3, 26): ("Good Friday", "none"),
    D(2027, 3, 27): ("Resurrection of Our Lord / Vigil of Easter", "white"),
    D(2027, 3, 28): ("Resurrection of Our Lord / Easter Day", "white"),
    D(2027, 4, 4): ("Second Sunday of Easter", "white"),
    D(2027, 5, 6): ("Ascension of Our Lord", "white"),
    D(2027, 5, 9): ("Seventh Sunday of Easter", "white"),
    D(2027, 5, 16): ("Day of Pentecost", "red"),
    D(2027, 5, 23): ("The Holy Trinity", "white"),
    D(2027, 5, 30): ("Second Sunday after Pentecost", "green"),
    D(2027, 11, 14): ("Twenty-sixth Sunday after Pentecost", "green"),
    D(2027, 11, 21): ("Christ the King", "white"),
}


@pytest.mark.parametrize(("date", "want"), NAMED_2026_27.items())
def test_named_days_2026_27(date, want):
    assert (cy.day_name(date), cy.color(date)) == want


@pytest.mark.parametrize(
    ("date", "want"),
    [
        (D(2023, 12, 24), "Fourth Sunday of Advent"),  # Dec 24 on a Sunday
        (D(2022, 12, 25), "Nativity of Our Lord / Christmas Day"),  # Christmas on a Sunday
        (D(2023, 1, 1), "First Sunday of Christmas"),  # ...so Jan 1 is the next Sunday
        (D(2030, 1, 6), "Epiphany of Our Lord"),  # Epiphany on a Sunday
        (D(2030, 1, 13), "Baptism of Our Lord"),  # ...so Baptism is the 13th
        (D(2027, 1, 7), None),  # an ordinary weekday
    ],
)
def test_named_day_edges(date, want):
    assert cy.day_name(date) == want


@pytest.mark.parametrize(
    ("date", "want"),
    [
        (D(2026, 11, 28), "A"),
        (D(2026, 11, 29), "B"),  # Advent 1, 2026 begins Year B
        (D(2027, 6, 1), "B"),
        (D(2027, 11, 28), "C"),
        (D(2028, 12, 3), "A"),
        (D(2025, 11, 30), "A"),
    ],
)
def test_rcl_year(date, want):
    assert cy.rcl_year(date) == want


@pytest.mark.parametrize(
    ("date", "want"),
    [
        (D(2026, 11, 22), 34),  # Christ the King 2026
        (D(2027, 11, 21), 34),  # Christ the King 2027
        (D(2027, 5, 30), 9),  # May 29-June 4
        (D(2027, 6, 6), 10),
        (D(2008, 5, 25), 8),  # May 24-28, only in years with an early Easter
        (D(2027, 5, 23), None),  # Holy Trinity has no number
        (D(2027, 6, 2), None),  # not a Sunday
        (D(2027, 1, 17), None),  # not after Pentecost
    ],
)
def test_lectionary_number(date, want):
    assert cy.lectionary_number(date) == want


@pytest.mark.parametrize(
    ("date", "want"),
    [
        (D(2026, 12, 24), "advent"),
        (D(2026, 12, 25), "christmas"),
        (D(2027, 1, 5), "christmas"),
        (D(2027, 1, 6), "time_after_epiphany"),
        (D(2027, 2, 10), "lent"),
        (D(2027, 3, 24), "lent"),
        (D(2027, 3, 25), "three_days"),
        (D(2027, 3, 27), "three_days"),
        (D(2027, 3, 28), "easter"),
        (D(2027, 5, 16), "easter"),
        (D(2027, 5, 17), "time_after_pentecost"),
    ],
)
def test_liturgical_season(date, want):
    assert cy.liturgical_season(date) == want


def test_church_day_on_a_weekday():
    day = cy.church_day(D(2026, 12, 2))
    assert day.name is None
    assert day.sunday == D(2026, 11, 29)
    assert day.sunday_name == "First Sunday of Advent"
    assert (day.season, day.season_name, day.color, day.rcl_year) == (
        "advent",
        "Advent",
        "blue",
        "B",
    )
    assert day.lectionary is None


def test_the_package_docstring_example():
    day = cy.church_day(D(2026, 12, 6))
    assert (day.name, day.rcl_year, day.color) == ("Second Sunday of Advent", "B", "blue")


def test_every_sunday_has_a_name_and_sensible_numbers_1900_to_2200():
    d = D(1900, 1, 7)  # a Sunday
    while d.year < 2200:
        name = cy.day_name(d)
        assert name, d
        assert cy.color(d) in cy.COLORS
        n = cy.lectionary_number(d)
        if n is not None:
            assert 8 <= n <= 34, d
        if name == "Christ the King":
            assert n == 34, d
            assert cy.advent_start(d.year) - d == dt.timedelta(days=7)
        d += dt.timedelta(days=7)


def test_every_day_has_a_season_and_color_for_two_years():
    d = D(2026, 1, 1)
    while d < D(2028, 1, 1):
        assert cy.liturgical_season(d) in cy.LITURGICAL_SEASONS
        assert cy.color(d) in cy.COLORS
        d += dt.timedelta(days=1)


def test_studio_seasons_and_church_seasons_agree_where_they_overlap():
    # Studio's "holyweek" is part of Lent and the Three Days; otherwise the two line up.
    same = {
        "advent": "advent",
        "christmas": "christmas",
        "epiphany": "time_after_epiphany",
        "lent": "lent",
        "easter": "easter",
    }
    d = D(2026, 1, 1)
    while d < D(2028, 1, 1):
        studio = cy.season(d)
        church = cy.liturgical_season(d)
        if studio in same:
            assert church == same[studio], d
        elif studio == "holyweek":
            assert church in ("lent", "three_days"), d
        else:  # Studio's "pentecost" includes Pentecost Day itself
            assert church in ("easter", "time_after_pentecost"), d
        d += dt.timedelta(days=1)
