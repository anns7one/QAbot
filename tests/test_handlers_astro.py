"""Tests for category selection and AI-personalized forecast generation."""
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock

from aiogram.types import InlineKeyboardMarkup

import bot.handlers_astro as handlers_astro
from bot.callbacks import CategoryCallback, ConfirmForecastCallback
from bot.contracts import is_valid_personal_message
from bot.handlers_astro import handle_category, handle_confirm_forecast
from bot.personal_message import FALLBACK_BODY
from bot.storage import Profile

PROFILE = Profile(
    user_id=123,
    name="Аня",
    birth_date=date(1995, 5, 17),
    level="middle",
    specialization="automation",
)


def make_callback(user_id: int = 123):
    return SimpleNamespace(
        from_user=SimpleNamespace(id=user_id),
        message=SimpleNamespace(answer=AsyncMock()),
        answer=AsyncMock(),
    )


def make_ai_client(response_text: str | None = None, raise_error: bool = False):
    async def generate_content(**kwargs):
        if raise_error:
            raise RuntimeError("Gemini is unavailable")
        return SimpleNamespace(text=response_text)

    models = SimpleNamespace(generate_content=generate_content)
    return SimpleNamespace(aio=SimpleNamespace(models=models))


async def test_handle_category_shows_confirm_button():
    callback = make_callback()

    await handle_category(callback, CategoryCallback(code="bug"))

    callback.answer.assert_awaited_once()
    callback.message.answer.assert_awaited_once()
    _, kwargs = callback.message.answer.await_args
    assert isinstance(kwargs["reply_markup"], InlineKeyboardMarkup)


async def test_handle_confirm_forecast_without_profile_asks_to_fill_one(monkeypatch):
    monkeypatch.setattr(handlers_astro, "get_profile", lambda user_id: None)
    callback = make_callback()

    await handle_confirm_forecast(callback, ConfirmForecastCallback(code="bug"), ai_client=None)

    callback.message.answer.assert_awaited_once()


async def test_handle_confirm_forecast_uses_fallback_when_ai_client_is_none(monkeypatch):
    monkeypatch.setattr(handlers_astro, "get_profile", lambda user_id: PROFILE)
    callback = make_callback()

    await handle_confirm_forecast(callback, ConfirmForecastCallback(code="motivation"), ai_client=None)

    first_call_text = callback.message.answer.await_args_list[0].args[0]
    assert FALLBACK_BODY in first_call_text
    assert is_valid_personal_message(first_call_text, PROFILE.name, "🔥 Мотивация на работу")


async def test_handle_confirm_forecast_uses_ai_response_on_success(monkeypatch):
    monkeypatch.setattr(handlers_astro, "get_profile", lambda user_id: PROFILE)
    callback = make_callback()
    ai_client = make_ai_client(response_text="Сегодня баги обойдут тебя стороной!")

    await handle_confirm_forecast(callback, ConfirmForecastCallback(code="bug"), ai_client=ai_client)

    first_call_text = callback.message.answer.await_args_list[0].args[0]
    assert "Сегодня баги обойдут тебя стороной!" in first_call_text


async def test_handle_confirm_forecast_falls_back_when_ai_call_raises(monkeypatch):
    monkeypatch.setattr(handlers_astro, "get_profile", lambda user_id: PROFILE)
    callback = make_callback()
    ai_client = make_ai_client(raise_error=True)

    await handle_confirm_forecast(callback, ConfirmForecastCallback(code="bug"), ai_client=ai_client)

    first_call_text = callback.message.answer.await_args_list[0].args[0]
    assert FALLBACK_BODY in first_call_text


async def test_handle_confirm_forecast_offers_another_category_afterwards(monkeypatch):
    monkeypatch.setattr(handlers_astro, "get_profile", lambda user_id: PROFILE)
    callback = make_callback()

    await handle_confirm_forecast(callback, ConfirmForecastCallback(code="bug"), ai_client=None)

    assert callback.message.answer.await_count == 2
    _, kwargs = callback.message.answer.await_args_list[1]
    assert isinstance(kwargs["reply_markup"], InlineKeyboardMarkup)
