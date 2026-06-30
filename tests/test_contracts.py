"""Contract tests: every rendered horoscope must satisfy the response-format
contract from the spec (ТЗ):
  - the string is not empty
  - it contains QA context
  - it does not break the expected format
"""
from datetime import date, timedelta

from bot.categories import get_category
from bot.contracts import (
    has_qa_context,
    is_valid_horoscope_text,
    is_valid_personal_message,
    matches_expected_structure,
)
from bot.horoscope import generate_horoscope
from bot.personal_message import render_personal_message
from bot.storage import Profile


def _render(user_id: int, horoscope_date: date) -> str:
    return generate_horoscope(user_id, horoscope_date).render()


def test_rendered_text_is_not_empty():
    text = _render(user_id=1, horoscope_date=date(2024, 1, 1))

    assert text.strip() != ""


def test_rendered_text_contains_qa_context():
    text = _render(user_id=1, horoscope_date=date(2024, 1, 1))

    assert has_qa_context(text)


def test_rendered_text_matches_expected_structure():
    text = _render(user_id=1, horoscope_date=date(2024, 1, 1))

    assert matches_expected_structure(text)


def test_structure_check_rejects_garbage_text():
    assert matches_expected_structure("just some random unrelated text") is False


def test_qa_context_check_rejects_text_without_qa_keywords():
    assert has_qa_context("просто случайный текст без контекста") is False


def test_contract_holds_for_many_users_and_dates():
    base_date = date(2024, 1, 1)

    for user_id in range(50):
        for day_offset in range(10):
            text = _render(user_id, base_date + timedelta(days=day_offset))
            assert is_valid_horoscope_text(text), text


def _make_profile() -> Profile:
    return Profile(
        user_id=1,
        name="Аня",
        birth_date=date(1995, 5, 17),
        level="middle",
        specialization="automation",
    )


def test_personal_message_contract_holds_for_every_category():
    profile = _make_profile()

    for category in get_category("bug"), get_category("support"):
        text = render_personal_message(profile, category, "Любой текст от AI или фолбэка.")
        assert is_valid_personal_message(text, profile.name, category.label), text


def test_personal_message_contract_rejects_text_without_name():
    assert is_valid_personal_message("🔮 Баг дня\n\nТекст", "Аня", "🐛 Баг дня") is False


def test_personal_message_contract_rejects_text_without_envelope_emoji():
    assert is_valid_personal_message("Баг дня для Ани\n\nТекст", "Аня", "🐛 Баг дня") is False
