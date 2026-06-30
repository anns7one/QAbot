"""Category selection and AI-personalized forecast generation."""
from __future__ import annotations

import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from google import genai

from bot.ai_advisor import generate_personal_message
from bot.callbacks import CategoryCallback, ConfirmForecastCallback
from bot.categories import get_category
from bot.keyboards import category_keyboard, confirm_forecast_keyboard
from bot.personal_message import FALLBACK_BODY, render_personal_message
from bot.storage import get_profile

logger = logging.getLogger(__name__)

router = Router(name="qa_astro")

NEXT_CATEGORY_TEXT = "Хочешь ещё один прогноз? Выбирай:"


@router.callback_query(CategoryCallback.filter())
async def handle_category(callback: CallbackQuery, callback_data: CategoryCallback) -> None:
    await callback.answer()
    category = get_category(callback_data.code)
    await callback.message.answer(
        f"Категория: {category.label}",
        reply_markup=confirm_forecast_keyboard(category.code),
    )


@router.callback_query(ConfirmForecastCallback.filter())
async def handle_confirm_forecast(
    callback: CallbackQuery,
    callback_data: ConfirmForecastCallback,
    ai_client: genai.Client | None,
) -> None:
    await callback.answer()
    profile = get_profile(callback.from_user.id)
    if profile is None:
        await callback.message.answer(
            "Профиль не найден — заполни его ещё раз через /start."
        )
        return

    category = get_category(callback_data.code)

    body = FALLBACK_BODY
    if ai_client is not None:
        try:
            body = await generate_personal_message(ai_client, profile, category)
        except Exception:
            logger.exception("Gemini call failed; using the static fallback message")

    await callback.message.answer(render_personal_message(profile, category, body))
    await callback.message.answer(NEXT_CATEGORY_TEXT, reply_markup=category_keyboard())
