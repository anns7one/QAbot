"""Tests for the QA-profile FSM flow (name -> birth date -> level -> specialization).

Uses a real aiogram FSMContext backed by in-memory storage, so the FSM
transitions themselves are exercised exactly as in production — only the
Telegram objects (Message/CallbackQuery) and the storage layer are faked.
"""
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage

import bot.handlers_profile as handlers_profile
from bot.callbacks import LevelCallback, SpecializationCallback
from bot.handlers_profile import (
    INVALID_BIRTH_DATE_TEXT,
    INVALID_NAME_TEXT,
    process_birth_date,
    process_level,
    process_name,
    process_specialization,
)
from bot.states import ProfileForm
from bot.storage import Profile


def make_state() -> FSMContext:
    storage = MemoryStorage()
    key = StorageKey(bot_id=1, chat_id=123, user_id=123)
    return FSMContext(storage=storage, key=key)


def make_message(text: str, user_id: int = 123):
    return SimpleNamespace(
        text=text,
        from_user=SimpleNamespace(id=user_id),
        answer=AsyncMock(),
    )


def make_callback(user_id: int = 123):
    return SimpleNamespace(
        from_user=SimpleNamespace(id=user_id),
        message=SimpleNamespace(answer=AsyncMock()),
        answer=AsyncMock(),
    )


async def test_process_name_rejects_empty_name():
    message = make_message("   ")
    state = make_state()

    await process_name(message, state)

    message.answer.assert_awaited_once_with(INVALID_NAME_TEXT)
    assert await state.get_state() is None


async def test_process_name_advances_to_birth_date_step():
    message = make_message("Аня")
    state = make_state()

    await process_name(message, state)

    assert await state.get_state() == ProfileForm.waiting_birth_date
    assert (await state.get_data())["name"] == "Аня"


async def test_process_birth_date_rejects_invalid_format():
    message = make_message("not-a-date")
    state = make_state()
    await state.set_state(ProfileForm.waiting_birth_date)

    await process_birth_date(message, state)

    message.answer.assert_awaited_once_with(INVALID_BIRTH_DATE_TEXT)
    assert await state.get_state() == ProfileForm.waiting_birth_date


async def test_process_birth_date_advances_to_level_step():
    message = make_message("17.05.1995")
    state = make_state()
    await state.set_state(ProfileForm.waiting_birth_date)

    await process_birth_date(message, state)

    assert await state.get_state() == ProfileForm.waiting_level
    assert (await state.get_data())["birth_date"] == "1995-05-17"


async def test_process_level_advances_to_specialization_step():
    callback = make_callback()
    state = make_state()
    await state.set_state(ProfileForm.waiting_level)

    await process_level(callback, LevelCallback(value="senior"), state)

    assert await state.get_state() == ProfileForm.waiting_specialization
    assert (await state.get_data())["level"] == "senior"


async def test_process_specialization_saves_profile_and_clears_state(
    monkeypatch,
):
    saved: list[Profile] = []
    monkeypatch.setattr(handlers_profile, "save_profile", saved.append)

    callback = make_callback(user_id=123)
    state = make_state()
    await state.set_state(ProfileForm.waiting_specialization)
    await state.update_data(name="Аня", birth_date="1995-05-17", level="senior")

    await process_specialization(callback, SpecializationCallback(value="api"), state)

    assert saved == [
        Profile(
            user_id=123,
            name="Аня",
            birth_date=date(1995, 5, 17),
            level="senior",
            specialization="api",
        )
    ]
    assert await state.get_state() is None
    callback.message.answer.assert_awaited_once()
