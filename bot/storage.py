"""Persistent storage for QA profiles (SQLite — no external DB service needed)."""
from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import date
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "profiles.db"


@dataclass(frozen=True)
class Profile:
    user_id: int
    name: str
    birth_date: date
    level: str
    specialization: str


def init_db(db_path: Path = DEFAULT_DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                level TEXT NOT NULL,
                specialization TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_profile(profile: Profile, db_path: Path = DEFAULT_DB_PATH) -> None:
    init_db(db_path)
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute(
            """
            INSERT INTO profiles (user_id, name, birth_date, level, specialization)
            VALUES (:user_id, :name, :birth_date, :level, :specialization)
            ON CONFLICT(user_id) DO UPDATE SET
                name = excluded.name,
                birth_date = excluded.birth_date,
                level = excluded.level,
                specialization = excluded.specialization
            """,
            {
                "user_id": profile.user_id,
                "name": profile.name,
                "birth_date": profile.birth_date.isoformat(),
                "level": profile.level,
                "specialization": profile.specialization,
            },
        )
        conn.commit()


def get_profile(user_id: int, db_path: Path = DEFAULT_DB_PATH) -> Profile | None:
    init_db(db_path)
    with closing(sqlite3.connect(db_path)) as conn:
        row = conn.execute(
            "SELECT user_id, name, birth_date, level, specialization "
            "FROM profiles WHERE user_id = ?",
            (user_id,),
        ).fetchone()
    if row is None:
        return None
    return Profile(
        user_id=row[0],
        name=row[1],
        birth_date=date.fromisoformat(row[2]),
        level=row[3],
        specialization=row[4],
    )
