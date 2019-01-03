import python_function as pf
from unittest import TestCase, mock

import datetime as dt


def test_breakfast_for_date():

    # Weekend case
    weekend_date = "2018-12-22"
    res = pf.breakfast_for_date(weekend_date)

    assert "No food is being served" in res

    # Weekday case
    weekday_date = "2018-12-20"
    with mock.patch("menu.BREAKFAST", {"2018-12-20": ["green eggs", "ham"]}):
        res = pf.breakfast_for_date(weekday_date)

        assert "today's breakfast menu" in res
        assert "green eggs" in res
        assert "also be ham" in res


def test_lunch_for_date():

    # Weekend case
    weekend_date = "2018-12-22"
    res = pf.lunch_for_date(weekend_date)

    assert "No food is being served" in res

    # Weekday case
    weekday_date = "2018-12-20"
    with mock.patch("menu.LUNCH", {"2018-12-20": "Pizza"}):
        res = pf.lunch_for_date(weekday_date)

        assert "today's lunch menu" in res
        assert "Pizza" in res
