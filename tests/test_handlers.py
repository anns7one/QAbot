"""Tests for the Telegram command handlers.

Handlers only call `message.answer(...)` and read `message.from_user.id`,
so a lightweight stand-in is enough — no need to construct a real
aiogram Message or spin up a Bot/Dispatcher.
"""
from types import SimpleNamespace
from unittest.mock import AsyncMock

from bot.contracts import is_valid_horoscope_text
from bot.handlers import START_TEXT, cmd_horoscope, cmd_start


def make_message(user_id: int = 123):
    return SimpleNamespace(
        from_user=SimpleNamespace(id=user_id),
        answer=AsyncMock(),
    )


async def test_cmd_start_sends_the_welcome_text():
    message = make_message()

    await cmd_start(message)

    message.answer.assert_awaited_once_with(START_TEXT)


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
