"""Application settings, loaded from environment variables / .env."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    gemini_api_key: str | None


def load_settings() -> Settings:
    """Read settings from the environment.

    Reads ``os.environ`` on every call (instead of caching a module-level
    singleton) so tests can freely monkeypatch env vars per-case.

    ``gemini_api_key`` is optional: without it the bot still runs, but the
    AI-personalized astro-regression flow falls back to a static message.
    """
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "BOT_TOKEN is not set. Copy .env.example to .env and fill in "
            "your bot token from @BotFather."
        )
    gemini_api_key = os.getenv("GEMINI_API_KEY") or None
    return Settings(bot_token=token, gemini_api_key=gemini_api_key)
