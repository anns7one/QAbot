"""Entry point: starts the QA Horoscope Bot in long-polling mode."""
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from google import genai

from bot.config import load_settings
from bot.handlers import router as main_router
from bot.handlers_astro import router as astro_router
from bot.handlers_profile import router as profile_router

logger = logging.getLogger(__name__)

BOT_COMMANDS = [
    BotCommand(command="start", description="Запустить бота"),
    BotCommand(command="horoscope", description="Получить QA-гороскоп на сегодня"),
]


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    settings = load_settings()
    bot = Bot(token=settings.bot_token)
    dispatcher = Dispatcher()
    dispatcher.include_router(main_router)
    dispatcher.include_router(profile_router)
    dispatcher.include_router(astro_router)

    ai_client: genai.Client | None = None
    if settings.gemini_api_key:
        ai_client = genai.Client(api_key=settings.gemini_api_key)
    else:
        logger.warning(
            "GEMINI_API_KEY is not set — personalized forecasts will use the "
            "static fallback message instead of calling Gemini."
        )

    try:
        await bot.set_my_commands(BOT_COMMANDS)
        await bot.delete_webhook(drop_pending_updates=True)

        logger.info("QA Horoscope Bot is starting (long polling)...")
        await dispatcher.start_polling(bot, ai_client=ai_client)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
