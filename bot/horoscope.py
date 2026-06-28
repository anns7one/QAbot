"""Core domain logic for generating the daily QA horoscope.

The generator is a pure function: given a user id and a calendar date it
deterministically returns the same Horoscope. This makes it trivial to
unit-test (no mocking of time/randomness needed) while still giving each
user a different, day-stable prediction.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date as date_type

QA_SIGNS: tuple[str, ...] = (
    "Баг-Хантер",
    "Регрессио",
    "Мок-Маг",
    "Скептик-Тестировщик",
    "Чек-лист Чародей",
    "Флаки-Тест Фараон",
    "CI/CD Провидец",
    "Эджкейс Эксперт",
)

PREDICTIONS: tuple[str, ...] = (
    "Сегодня прод выдержит даже смелый релиз, но смоук-тест проведи дважды.",
    "Меркурий в ретрограде — жди flaky-тест в самый неподходящий момент.",
    "Звёзды советуют написать тест-кейс, прежде чем разработчик скажет "
    "«тут и так всё понятно».",
    "Баг, которого ты боишься, прячется в граничном значении. Проверь edge case.",
    "Сегодня удачный день для рефакторинга автотестов — техдолг отступит.",
    "Придёт баг-репорт без шагов воспроизведения. Сохраняй спокойствие и проси логи.",
    "Регрессия будет благосклонна, если покроешь критический путь тестами.",
    "Сегодня хороший день, чтобы наконец убрать skip с того теста.",
    "CI обещает быть зелёным, если актуализируешь тестовые данные.",
    "Документация соврёт хотя бы раз — доверяй, но проверяй в коде.",
)

ADVICE: tuple[str, ...] = (
    "Пиши тест на каждый баг, который нашёл вручную.",
    "Не доверяй фразе «это же очевидно работает» — проверь сам.",
    "Сделай бэкап тестовых данных перед экспериментами.",
    "Запусти полный регрессионный набор перед релизом.",
    "Добавь логирование туда, где сейчас тишина.",
    "Раз в день читай changelog зависимостей — сюрпризов будет меньше.",
)


@dataclass(frozen=True)
class Horoscope:
    """Structured horoscope result, independent of how it gets rendered."""

    sign: str
    prediction: str
    advice: str
    horoscope_date: date_type

    def render(self) -> str:
        """Render the horoscope as the exact text sent to the user."""
        return (
            f"🔮 QA-гороскоп на {self.horoscope_date.isoformat()}\n"
            "\n"
            f"Знак: {self.sign}\n"
            f"{self.prediction}\n"
            "\n"
            f"Совет дня: {self.advice}"
        )


def generate_horoscope(user_id: int, horoscope_date: date_type) -> Horoscope:
    """Generate a horoscope that is stable for the same user on the same date.

    Uses a seeded RNG (seeded from ``user_id`` + ``horoscope_date``) instead of
    global randomness, so the same call always returns the same result —
    no mocking of ``random`` or the clock is required in tests.
    """
    seed = f"{user_id}:{horoscope_date.isoformat()}"
    rng = random.Random(seed)
    return Horoscope(
        sign=rng.choice(QA_SIGNS),
        prediction=rng.choice(PREDICTIONS),
        advice=rng.choice(ADVICE),
        horoscope_date=horoscope_date,
    )
