"""Inline keyboards for the QA profile + astro-regression flow."""
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks import (
    CategoryCallback,
    ConfirmForecastCallback,
    LevelCallback,
    MenuCallback,
    SpecializationCallback,
)
from bot.categories import CATEGORIES
from bot.profile_options import LEVELS, SPECIALIZATIONS


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="📝 Заполнить QA профиль",
        callback_data=MenuCallback(action="fill_profile"),
    )
    builder.button(
        text="🌌 Пройти астрорегрессию",
        callback_data=MenuCallback(action="start_astro"),
    )
    builder.adjust(1)
    return builder.as_markup()


def level_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for code, label in LEVELS:
        builder.button(text=label, callback_data=LevelCallback(value=code))
    builder.adjust(2)
    return builder.as_markup()


def specialization_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for code, label in SPECIALIZATIONS:
        builder.button(text=label, callback_data=SpecializationCallback(value=code))
    builder.adjust(2)
    return builder.as_markup()


def category_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for category in CATEGORIES:
        builder.button(text=category.label, callback_data=CategoryCallback(code=category.code))
    builder.adjust(1)
    return builder.as_markup()


def confirm_forecast_keyboard(category_code: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔮 Получить персональный прогноз",
        callback_data=ConfirmForecastCallback(code=category_code),
    )
    return builder.as_markup()
