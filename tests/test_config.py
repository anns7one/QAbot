"""Tests for environment-based settings loading (bot/config.py)."""
import pytest

from bot.config import load_settings


def test_load_settings_reads_token_from_env(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    settings = load_settings()

    assert settings.bot_token == "test-token"


def test_load_settings_raises_a_clear_error_without_a_token(monkeypatch):
    monkeypatch.delenv("BOT_TOKEN", raising=False)

    with pytest.raises(RuntimeError):
        load_settings()


def test_load_settings_gemini_api_key_is_none_when_unset(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    settings = load_settings()

    assert settings.gemini_api_key is None


def test_load_settings_reads_gemini_api_key_from_env(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-key")

    settings = load_settings()

    assert settings.gemini_api_key == "test-gemini-key"
