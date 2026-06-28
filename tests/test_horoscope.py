"""Unit tests for the horoscope generation logic (bot/horoscope.py)."""
from datetime import date

from bot.horoscope import ADVICE, PREDICTIONS, QA_SIGNS, generate_horoscope

FIXED_DATE = date(2024, 5, 17)


def test_generate_horoscope_is_deterministic_for_same_user_and_date():
    first = generate_horoscope(user_id=42, horoscope_date=FIXED_DATE)
    second = generate_horoscope(user_id=42, horoscope_date=FIXED_DATE)

    assert first == second


def test_generate_horoscope_stores_the_requested_date():
    horoscope = generate_horoscope(user_id=1, horoscope_date=FIXED_DATE)

    assert horoscope.horoscope_date == FIXED_DATE


def test_generate_horoscope_fields_come_from_known_pools():
    horoscope = generate_horoscope(user_id=7, horoscope_date=FIXED_DATE)

    assert horoscope.sign in QA_SIGNS
    assert horoscope.prediction in PREDICTIONS
    assert horoscope.advice in ADVICE


def test_generate_horoscope_varies_across_dates_for_the_same_user():
    results = {
        generate_horoscope(user_id=1, horoscope_date=date(2024, 1, day))
        for day in range(1, 28)
    }

    assert len(results) > 1


def test_generate_horoscope_varies_across_users_for_the_same_date():
    results = {
        generate_horoscope(user_id=user_id, horoscope_date=FIXED_DATE)
        for user_id in range(50)
    }

    assert len(results) > 1


def test_render_includes_all_fields_of_the_horoscope():
    horoscope = generate_horoscope(user_id=99, horoscope_date=FIXED_DATE)
    text = horoscope.render()

    assert horoscope.sign in text
    assert horoscope.prediction in text
    assert horoscope.advice in text
    assert horoscope.horoscope_date.isoformat() in text
