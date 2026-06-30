"""Pure date -> Western zodiac sign lookup, used to flavor AI prompts."""
from __future__ import annotations

from datetime import date

# Each entry is the (month, day) of the LAST day of that sign's range.
# Sorted by that cutoff date; a date falls into the first cutoff it is <= to,
# wrapping around to Capricorn for anything after Dec 21.
_SIGN_CUTOFFS: tuple[tuple[int, int, str], ...] = (
    (1, 19, "Козерог"),
    (2, 18, "Водолей"),
    (3, 20, "Рыбы"),
    (4, 19, "Овен"),
    (5, 20, "Телец"),
    (6, 20, "Близнецы"),
    (7, 22, "Рак"),
    (8, 22, "Лев"),
    (9, 22, "Дева"),
    (10, 22, "Весы"),
    (11, 21, "Скорпион"),
    (12, 21, "Стрелец"),
)
_LAST_SIGN_OF_YEAR = "Козерог"


def zodiac_sign(birth_date: date) -> str:
    """Return the Western zodiac sign name (in Russian) for a birth date."""
    month_day = (birth_date.month, birth_date.day)
    for cutoff_month, cutoff_day, sign in _SIGN_CUTOFFS:
        if month_day <= (cutoff_month, cutoff_day):
            return sign
    return _LAST_SIGN_OF_YEAR
