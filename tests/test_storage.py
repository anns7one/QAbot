"""Unit tests for bot/storage.py (SQLite-backed QA profile storage)."""
from datetime import date
from pathlib import Path

from bot.storage import Profile, get_profile, save_profile


def _make_profile(user_id: int = 1) -> Profile:
    return Profile(
        user_id=user_id,
        name="Аня",
        birth_date=date(1995, 5, 17),
        level="middle",
        specialization="automation",
    )


def test_get_profile_returns_none_when_missing(tmp_path: Path):
    db_path = tmp_path / "profiles.db"

    assert get_profile(1, db_path=db_path) is None


def test_save_and_get_profile_roundtrip(tmp_path: Path):
    db_path = tmp_path / "profiles.db"
    profile = _make_profile()

    save_profile(profile, db_path=db_path)
    loaded = get_profile(profile.user_id, db_path=db_path)

    assert loaded == profile


def test_save_profile_upserts_existing_user(tmp_path: Path):
    db_path = tmp_path / "profiles.db"
    save_profile(_make_profile(), db_path=db_path)

    updated = Profile(
        user_id=1,
        name="Анна",
        birth_date=date(1995, 5, 17),
        level="senior",
        specialization="api",
    )
    save_profile(updated, db_path=db_path)

    loaded = get_profile(1, db_path=db_path)
    assert loaded == updated


def test_profiles_for_different_users_are_independent(tmp_path: Path):
    db_path = tmp_path / "profiles.db"
    save_profile(_make_profile(user_id=1), db_path=db_path)
    save_profile(_make_profile(user_id=2), db_path=db_path)

    assert get_profile(1, db_path=db_path).user_id == 1
    assert get_profile(2, db_path=db_path).user_id == 2
