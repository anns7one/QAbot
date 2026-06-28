"""Telegram command handlers: /start and /horoscope."""
from __future__ import annotations

from datetime import date

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.horoscope import generate_horoscope

router = Router(name="qa_horoscope")

START_TEXT = (
    "Привет! Я QA Horoscope Bot 🔮\n"
    "Каждый день предсказываю QA-судьбу: баги, регрессии и flaky-тесты.\n"
    "\n"
    "Команды:\n"
    "/horoscope — получить гороскоп на сегодня"
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(START_TEXT)


@router.message(Command("horoscope"))
async def cmd_horoscope(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    horoscope = generate_horoscope(user_id, date.today())
    await message.answer(horoscope.render())
