"""Generates a personalized astrology + psychological-support message via Gemini.

Kept separate from the handler so the prompt and the API call are unit-testable
without touching Telegram or the network: pass in a fake client and assert on
the prompt or the parsed result.
"""
from __future__ import annotations

from google import genai
from google.genai import types

from bot.categories import Category
from bot.storage import Profile
from bot.zodiac import zodiac_sign

MODEL_NAME = "gemini-3.5-flash"

SYSTEM_INSTRUCTION = (
    "Ты — тёплый и проницательный астролог-психолог, который специализируется "
    "на поддержке QA-инженеров. Ты совмещаешь лёгкий астрологический колорит "
    "с практической психологической поддержкой и юмором про тестирование. "
    "Обращайся к человеку по имени, пиши по-русски, без markdown-разметки, "
    "не более 120 слов, заканчивай одной конкретной рекомендацией."
)


def build_prompt(profile: Profile, category: Category) -> str:
    sign = zodiac_sign(profile.birth_date)
    return (
        f"Имя: {profile.name}\n"
        f"Знак зодиака: {sign}\n"
        f"Уровень: {profile.level}\n"
        f"Специализация: {profile.specialization}\n"
        f"Запрос: {category.label} — {category.prompt_hint}.\n"
        "Сгенерируй персональное послание под этот запрос."
    )


async def generate_personal_message(
    client: genai.Client, profile: Profile, category: Category
) -> str:
    """Ask Gemini for a personalized message.

    Raises on any failure (empty response, API error) — the caller decides
    what fallback to show the user instead of swallowing errors here.
    """
    response = await client.aio.models.generate_content(
        model=MODEL_NAME,
        contents=build_prompt(profile, category),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.9,
            max_output_tokens=400,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise ValueError("Gemini returned an empty response")
    return text
