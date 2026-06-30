"""Typed callback_data payloads for inline keyboards (aiogram CallbackData)."""
from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class MenuCallback(CallbackData, prefix="menu"):
    action: str  # "fill_profile" | "start_astro"


class LevelCallback(CallbackData, prefix="level"):
    value: str


class SpecializationCallback(CallbackData, prefix="spec"):
    value: str


class CategoryCallback(CallbackData, prefix="cat"):
    code: str


class ConfirmForecastCallback(CallbackData, prefix="confirm"):
    code: str
