"""Unit tests for bot/zodiac.py."""
from datetime import date

import pytest

from bot.zodiac import zodiac_sign


@pytest.mark.parametrize(
    "birth_date, expected_sign",
    [
        (date(2000, 1, 1), "Козерог"),
        (date(2000, 1, 19), "Козерог"),
        (date(2000, 1, 20), "Водолей"),
        (date(2000, 2, 18), "Водолей"),
        (date(2000, 2, 19), "Рыбы"),
        (date(2000, 3, 21), "Овен"),
        (date(2000, 4, 20), "Телец"),
        (date(2000, 5, 21), "Близнецы"),
        (date(2000, 6, 21), "Рак"),
        (date(2000, 7, 23), "Лев"),
        (date(2000, 8, 23), "Дева"),
        (date(2000, 9, 23), "Весы"),
        (date(2000, 10, 23), "Скорпион"),
        (date(2000, 11, 22), "Стрелец"),
        (date(2000, 12, 21), "Стрелец"),
        (date(2000, 12, 22), "Козерог"),
        (date(2000, 12, 31), "Козерог"),
    ],
)
def test_zodiac_sign_boundaries(birth_date: date, expected_sign: str):
    assert zodiac_sign(birth_date) == expected_sign
