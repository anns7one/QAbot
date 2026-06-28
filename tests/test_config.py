"""Tests for environment-based settings loading (bot/config.py)."""
import pytest

from bot.config import load_settings


def test_load_settings_reads_token_from_env(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "test-token")

    settings = load_settings()

    assert settings.bot_token == "test-token"


def test_load_settings_raises_a_clear_error_without_a_token(monkeypatch):
    monkeypatch.delenv("BOT_TOKEN", raising=False)

    with pytest.raises(RuntimeError):
        load_settings()
