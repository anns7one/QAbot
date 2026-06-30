"""Renders the final personalized astro-regression message (envelope + body).

The envelope (header with category + name) is fixed and deterministic so it
stays contract-testable; only the body in between comes from the AI (or the
static fallback when the AI is unavailable).
"""
from __future__ import annotations

from bot.categories import Category
from bot.storage import Profile

FALLBACK_BODY = (
    "Не получилось дотянуться до звёзд (и до Gemini) прямо сейчас. "
    "Попробуй ещё раз через пару минут — а пока ты молодец уже за то, "
    "что разбираешься со своими тестами!"
)


def render_personal_message(profile: Profile, category: Category, body: str) -> str:
    return f"🔮 {category.label} для {profile.name}\n" "\n" f"{body}"
