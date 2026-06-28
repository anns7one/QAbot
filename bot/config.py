"""Application settings, loaded from environment variables / .env."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str


def load_settings() -> Settings:
    """Read settings from the environment.

    Reads ``os.environ`` on every call (instead of caching a module-level
    singleton) so tests can freely monkeypatch ``BOT_TOKEN`` per-case.
    """
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "BOT_TOKEN is not set. Copy .env.example to .env and fill in "
            "your bot token from @BotFather."
        )
    return Settings(bot_token=token)
