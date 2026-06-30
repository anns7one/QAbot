"""Registry of QA-horoscope request categories.

Adding a new category is a one-line addition here — nothing else needs to
change, since keyboards and AI prompts are both built from this tuple.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    code: str
    label: str
    prompt_hint: str


CATEGORIES: tuple[Category, ...] = (
    Category(
        "bug",
        "🐛 Баг дня",
        "юмористическое предсказание о баге, который может встретиться сегодня, и как его избежать",
    ),
    Category(
        "career",
        "📈 Карьерный прогноз",
        "прогноз по карьерному росту в QA",
    ),
    Category(
        "finance",
        "💰 Финансы",
        "прогноз по финансовым делам",
    ),
    Category(
        "love",
        "❤️ Личная жизнь",
        "прогноз по личной жизни и отношениям",
    ),
    Category(
        "energy",
        "⚡ Энергия и настроение",
        "прогноз настроения и уровня энергии на день",
    ),
    Category(
        "team",
        "🤝 Отношения с командой",
        "совет по отношениям с командой и коллегами",
    ),
    Category(
        "advice",
        "💡 Советы по работе",
        "практический совет по рабочим QA-задачам",
    ),
    Category(
        "motivation",
        "🔥 Мотивация на работу",
        "мотивационное послание для рабочего дня",
    ),
    Category(
        "support",
        "🧘 Успокоение и поддержка",
        "тёплая психологическая поддержка, особенно если на работе случился неприятный инцидент",
    ),
)

_BY_CODE = {category.code: category for category in CATEGORIES}


def get_category(code: str) -> Category:
    try:
        return _BY_CODE[code]
    except KeyError:
        raise ValueError(f"Unknown category code: {code}") from None
