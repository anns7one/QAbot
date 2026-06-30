"""FSM steps for filling in the QA profile (name -> birth date -> level -> specialization)."""
from __future__ import annotations

from datetime import date, datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import LevelCallback, SpecializationCallback
from bot.keyboards import category_keyboard, level_keyboard, specialization_keyboard
from bot.states import ProfileForm
from bot.storage import Profile, save_profile

router = Router(name="qa_profile_form")

MAX_NAME_LENGTH = 50
BIRTH_DATE_FORMAT = "%d.%m.%Y"

INVALID_NAME_TEXT = f"Имя не должно быть пустым (и короче {MAX_NAME_LENGTH} символов). Попробуй ещё раз:"
ASK_BIRTH_DATE_TEXT = "Когда у тебя день рождения? Формат: ДД.ММ.ГГГГ, например 17.05.1995"
INVALID_BIRTH_DATE_TEXT = "Не получилось распознать дату. Формат: ДД.ММ.ГГГГ, например 17.05.1995"
ASK_LEVEL_TEXT = "Какой у тебя уровень?"
ASK_SPECIALIZATION_TEXT = "А специализация?"
PROFILE_SAVED_TEXT = "Профиль сохранён! Что хочешь получить сегодня?"


@router.message(ProfileForm.waiting_name, F.text)
async def process_name(message: Message, state: FSMContext) -> None:
    name = (message.text or "").strip()
    if not name or len(name) > MAX_NAME_LENGTH:
        await message.answer(INVALID_NAME_TEXT)
        return
    await state.update_data(name=name)
    await state.set_state(ProfileForm.waiting_birth_date)
    await message.answer(ASK_BIRTH_DATE_TEXT)


@router.message(ProfileForm.waiting_birth_date, F.text)
async def process_birth_date(message: Message, state: FSMContext) -> None:
    try:
        birth_date = datetime.strptime((message.text or "").strip(), BIRTH_DATE_FORMAT).date()
    except ValueError:
        await message.answer(INVALID_BIRTH_DATE_TEXT)
        return
    await state.update_data(birth_date=birth_date.isoformat())
    await state.set_state(ProfileForm.waiting_level)
    await message.answer(ASK_LEVEL_TEXT, reply_markup=level_keyboard())


@router.callback_query(ProfileForm.waiting_level, LevelCallback.filter())
async def process_level(
    callback: CallbackQuery, callback_data: LevelCallback, state: FSMContext
) -> None:
    await callback.answer()
    await state.update_data(level=callback_data.value)
    await state.set_state(ProfileForm.waiting_specialization)
    await callback.message.answer(ASK_SPECIALIZATION_TEXT, reply_markup=specialization_keyboard())


@router.callback_query(ProfileForm.waiting_specialization, SpecializationCallback.filter())
async def process_specialization(
    callback: CallbackQuery, callback_data: SpecializationCallback, state: FSMContext
) -> None:
    await callback.answer()
    data = await state.get_data()
    profile = Profile(
        user_id=callback.from_user.id,
        name=data["name"],
        birth_date=date.fromisoformat(data["birth_date"]),
        level=data["level"],
        specialization=callback_data.value,
    )
    save_profile(profile)
    await state.clear()
    await callback.message.answer(PROFILE_SAVED_TEXT, reply_markup=category_keyboard())
