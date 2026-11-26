import datetime as dt

import churchyear as cy


def test_every_row_is_a_real_date_with_a_known_rank():
    rows = cy.all_commemorations()
    assert len(rows) > 100
    for c in rows:
        dt.date(2024, c.month, c.day)  # 2024 is a leap year, so Feb 29 would be allowed
        assert c.rank in ("lesser festival", "commemoration")
        assert c.name.strip() == c.name and c.name


def test_unchecked_rows_are_left_out_unless_asked_for():
    andrew = dt.date(2026, 11, 30)
    unchecked = [c for c in cy.all_commemorations() if not c.checked]
    if unchecked:
        assert all(c.checked for c in cy.commemorations_on(andrew))
    names = [c.name for c in cy.commemorations_on(andrew, include_unchecked=True)]
    assert names == ["Andrew, Apostle"]


def test_church_day_lists_only_checked_commemorations():
    day = cy.church_day(dt.date(2026, 11, 30))
    assert all(c.checked for c in day.commemorations)


def test_no_principal_festivals_in_the_file():
    # Christmas, Epiphany and the rest are worked out in code, not listed here.
    names = {c.name for c in cy.all_commemorations()}
    assert not any("Nativity" in n or n.startswith("Epiphany") for n in names)
