"""Tests for the Telegram command handlers.

Handlers only call `message.answer(...)` / `callback.answer(...)` and read
`message.from_user.id`, so lightweight stand-ins are enough — no need to
construct a real aiogram Message/CallbackQuery or spin up a Bot/Dispatcher.
"""
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from aiogram.types import InlineKeyboardMarkup

import bot.handlers as handlers
from bot.callbacks import MenuCallback
from bot.contracts import is_valid_horoscope_text
from bot.handlers import NEED_PROFILE_TEXT, START_TEXT, cmd_horoscope, cmd_start, handle_menu
from bot.storage import Profile


def make_message(user_id: int = 123):
    return SimpleNamespace(
        from_user=SimpleNamespace(id=user_id),
        answer=AsyncMock(),
    )


def make_callback(user_id: int = 123):
    return SimpleNamespace(
        from_user=SimpleNamespace(id=user_id),
        message=make_message(user_id),
        answer=AsyncMock(),
    )


def make_state():
    return SimpleNamespace(set_state=AsyncMock())


async def test_cmd_start_sends_the_welcome_text_with_main_menu():
    message = make_message()

    await cmd_start(message)

    message.answer.assert_awaited_once()
    args, kwargs = message.answer.await_args
    assert args[0] == START_TEXT
    assert isinstance(kwargs["reply_markup"], InlineKeyboardMarkup)


async def test_cmd_horoscope_sends_a_contract_valid_message():
    message = make_message()

    await cmd_horoscope(message)

    message.answer.assert_awaited_once()
    sent_text = message.answer.await_args.args[0]
    assert is_valid_horoscope_text(sent_text)


async def test_cmd_horoscope_works_without_a_from_user():
    message = make_message()
    message.from_user = None

    await cmd_horoscope(message)

    message.answer.assert_awaited_once()


async def test_cmd_horoscope_is_stable_for_the_same_user_within_a_call():
    message = make_message(user_id=7)

    await cmd_horoscope(message)
    first_text = message.answer.await_args.args[0]

    await cmd_horoscope(message)
    second_text = message.answer.await_args.args[0]

    assert first_text == second_text


async def test_handle_menu_fill_profile_starts_the_form():
    callback = make_callback()
    state = make_state()

    await handle_menu(callback, MenuCallback(action="fill_profile"), state)

    callback.answer.assert_awaited_once()
    state.set_state.assert_awaited_once()
    callback.message.answer.assert_awaited_once()


async def test_handle_menu_start_astro_without_profile_asks_to_fill_it(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(handlers, "get_profile", lambda user_id: None)
    callback = make_callback()
    state = make_state()

    await handle_menu(callback, MenuCallback(action="start_astro"), state)

    callback.message.answer.assert_awaited_once()
    assert callback.message.answer.await_args.args[0] == NEED_PROFILE_TEXT


async def test_handle_menu_start_astro_with_profile_shows_category_menu(
    monkeypatch: pytest.MonkeyPatch,
):
    profile = Profile(
        user_id=123,
        name="Аня",
        birth_date=None,  # not read on this path
        level="middle",
        specialization="automation",
    )
    monkeypatch.setattr(handlers, "get_profile", lambda user_id: profile)
    callback = make_callback()
    state = make_state()

    await handle_menu(callback, MenuCallback(action="start_astro"), state)

    callback.message.answer.assert_awaited_once()
    _, kwargs = callback.message.answer.await_args
    assert isinstance(kwargs["reply_markup"], InlineKeyboardMarkup)
