"""The response-format contract that every horoscope message must satisfy.

Kept separate from ``horoscope.py`` so the contract is a reusable, named
thing: tests assert against it, and any future producer of horoscope text
(a new command, an admin preview endpoint, etc.) can validate against the
same rules instead of re-implementing them.
"""
from __future__ import annotations

import re

QA_CONTEXT_KEYWORDS: tuple[str, ...] = (
    "qa",
    "баг",
    "тест",
    "регресс",
    "релиз",
    "ci",
)

_STRUCTURE_PATTERN = re.compile(
    r"^🔮 QA-гороскоп на \d{4}-\d{2}-\d{2}\n"
    r"\n"
    r"Знак: [^\n]+\n"
    r"[^\n]+\n"
    r"\n"
    r"Совет дня: [^\n]+$"
)


def has_qa_context(text: str) -> bool:
    """Return True if the text clearly reads as QA-flavored content."""
    lowered = text.lower()
    return any(keyword in lowered for keyword in QA_CONTEXT_KEYWORDS)


def matches_expected_structure(text: str) -> bool:
    """Return True if the text follows the fixed horoscope layout."""
    return _STRUCTURE_PATTERN.match(text) is not None


def is_valid_horoscope_text(text: str) -> bool:
    """Full contract: non-empty, QA-flavored, and correctly formatted."""
    if not text or not text.strip():
        return False
    if not has_qa_context(text):
        return False
    if not matches_expected_structure(text):
        return False
    return True


def is_valid_personal_message(text: str, name: str, category_label: str) -> bool:
    """Contract for AI-personalized messages: non-empty envelope, right shape.

    Unlike ``is_valid_horoscope_text`` this does not pin down the AI-written
    body content — only the deterministic envelope (emoji header, category,
    name) that ``bot/personal_message.py`` always produces regardless of
    whether the body came from the AI or the static fallback.
    """
    if not text or not text.strip():
        return False
    if not text.startswith("🔮"):
        return False
    if name not in text:
        return False
    if category_label not in text:
        return False
    return True
