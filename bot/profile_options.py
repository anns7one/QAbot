"""Registries of selectable QA profile options (level, specialization)."""
from __future__ import annotations

LEVELS: tuple[tuple[str, str], ...] = (
    ("junior", "Junior"),
    ("middle", "Middle"),
    ("senior", "Senior"),
    ("lead", "Lead"),
)

SPECIALIZATIONS: tuple[tuple[str, str], ...] = (
    ("web", "🌐 Web"),
    ("mobile", "📱 Mobile"),
    ("api", "🔌 API"),
    ("automation", "🤖 Automation"),
    ("fullstack", "🧩 Fullstack"),
)

_LEVEL_LABELS = dict(LEVELS)
_SPECIALIZATION_LABELS = dict(SPECIALIZATIONS)


def level_label(code: str) -> str:
    return _LEVEL_LABELS.get(code, code)


def specialization_label(code: str) -> str:
    return _SPECIALIZATION_LABELS.get(code, code)
