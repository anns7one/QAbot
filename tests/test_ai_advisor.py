"""Unit tests for bot/ai_advisor.py, using a fake Gemini client (no network)."""
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from bot.ai_advisor import build_prompt, generate_personal_message
from bot.categories import get_category
from bot.storage import Profile

PROFILE = Profile(
    user_id=1,
    name="Аня",
    birth_date=date(1995, 5, 17),
    level="middle",
    specialization="automation",
)


def make_fake_client(response_text: str):
    fake_response = SimpleNamespace(text=response_text)
    fake_models = SimpleNamespace(generate_content=AsyncMock(return_value=fake_response))
    return SimpleNamespace(aio=SimpleNamespace(models=fake_models))


def test_build_prompt_includes_profile_and_category_details():
    category = get_category("career")

    prompt = build_prompt(PROFILE, category)

    assert PROFILE.name in prompt
    assert PROFILE.level in prompt
    assert PROFILE.specialization in prompt
    assert category.label in prompt
    assert "Телец" in prompt  # zodiac sign for May 17


async def test_generate_personal_message_returns_stripped_text():
    client = make_fake_client("  Отличный день для тестов!  ")
    category = get_category("motivation")

    result = await generate_personal_message(client, PROFILE, category)

    assert result == "Отличный день для тестов!"
    client.aio.models.generate_content.assert_awaited_once()


async def test_generate_personal_message_raises_on_empty_response():
    client = make_fake_client("   ")
    category = get_category("motivation")

    with pytest.raises(ValueError):
        await generate_personal_message(client, PROFILE, category)
