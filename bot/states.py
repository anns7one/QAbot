"""FSM states for the multi-step QA profile form."""
from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class ProfileForm(StatesGroup):
    waiting_name = State()
    waiting_birth_date = State()
    waiting_level = State()
    waiting_specialization = State()
