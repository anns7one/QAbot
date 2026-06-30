"""Telegram command handlers: /start, /horoscope, and the main-menu buttons."""
from __future__ import annotations

from datetime import date

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import MenuCallback
from bot.horoscope import generate_horoscope
from bot.keyboards import category_keyboard, main_menu_keyboard
from bot.states import ProfileForm
from bot.storage import get_profile

router = Router(name="qa_horoscope")

START_TEXT = (
    "Привет! Я QA Horoscope Bot 🔮\n"
    "Каждый день предсказываю QA-судьбу: баги, регрессии и flaky-тесты.\n"
    "А ещё умею делать персональный астро-прогноз с поддержкой — для этого "
    "нужно один раз заполнить QA профиль.\n"
    "\n"
    "Команды:\n"
    "/horoscope — короткий гороскоп на сегодня без профиля"
)

NEED_PROFILE_TEXT = (
    "Чтобы пройти астрорегрессию, сначала заполни QA профиль — это займёт "
    "меньше минуты."
)

ASK_CATEGORY_TEXT = "Что хочешь получить сегодня?"


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(START_TEXT, reply_markup=main_menu_keyboard())


@router.message(Command("horoscope"))
async def cmd_horoscope(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    horoscope = generate_horoscope(user_id, date.today())
    await message.answer(horoscope.render())


@router.callback_query(MenuCallback.filter())
async def handle_menu(callback: CallbackQuery, callback_data: MenuCallback, state: FSMContext) -> None:
    await callback.answer()
    user_id = callback.from_user.id

    if callback_data.action == "fill_profile":
        await state.set_state(ProfileForm.waiting_name)
        await callback.message.answer("Как тебя зовут?")
        return

    if callback_data.action == "start_astro":
        if get_profile(user_id) is None:
            await callback.message.answer(NEED_PROFILE_TEXT, reply_markup=main_menu_keyboard())
            return
        await callback.message.answer(ASK_CATEGORY_TEXT, reply_markup=category_keyboard())
