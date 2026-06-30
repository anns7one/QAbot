# QAbot — QA Horoscope Bot

Telegram-бот для QA-инженеров с двумя режимами:

- **`/horoscope`** — короткий детерминированный гороскоп без профиля. Один
  и тот же пользователь в течение одного дня всегда получает один и тот же
  результат (никакого профиля заполнять не нужно).
- **«Пройти астрорегрессию»** — персональный AI-прогноз/психологическая
  поддержка на основе QA-профиля (имя, дата рождения, уровень,
  специализация) и выбранной категории (баг дня, карьера, финансы,
  личная жизнь, энергия и настроение, отношения с командой, советы по
  работе, мотивация, успокоение и поддержка). Текст генерирует Google
  Gemini; если AI недоступен — бот не падает, а отвечает заготовленным
  текстом.

## Стек

- Python 3.11
- [aiogram v3](https://docs.aiogram.dev/) — Telegram Bot API framework
- [google-genai](https://googleapis.github.io/python-genai/) — клиент Gemini API (бесплатный тариф)
- SQLite (стандартная библиотека) — хранение QA-профилей
- pytest + pytest-asyncio — автотесты
- Docker + docker-compose
- python-dotenv — конфигурация через `.env`

## Структура проекта

```
bot/
  __init__.py
  config.py             # настройки из окружения (BOT_TOKEN, GEMINI_API_KEY)
  contracts.py            # контракты формата ответа (гороскоп + персональное сообщение)
  horoscope.py             # детерминированный генератор /horoscope
  zodiac.py                # дата рождения -> знак зодиака (чистая функция)
  storage.py                # SQLite-хранилище QA-профилей
  categories.py              # реестр категорий астрорегрессии (легко расширять)
  profile_options.py          # реестр уровней/специализаций
  callbacks.py                 # типизированные callback_data для inline-кнопок
  keyboards.py                  # inline-клавиатуры
  states.py                      # FSM-состояния формы профиля
  ai_advisor.py                   # вызов Gemini + сборка промпта
  personal_message.py               # рендер финального сообщения (конверт + текст)
  handlers.py                        # /start, /horoscope, главное меню
  handlers_profile.py                 # FSM-шаги заполнения профиля
  handlers_astro.py                    # выбор категории + вызов AI
tests/
  test_config.py
  test_contracts.py
  test_horoscope.py
  test_zodiac.py
  test_categories.py
  test_storage.py
  test_ai_advisor.py
  test_handlers.py
  test_handlers_profile.py
  test_handlers_astro.py
main.py                                 # точка входа, long polling
Dockerfile
docker-compose.yml
requirements.txt                          # runtime-зависимости
requirements-dev.txt                       # + зависимости для тестов
data/                                       # SQLite-файл профилей (создаётся сам, не в git)
```

## Быстрый старт (локально, без Docker)

1. Создай и активируй виртуальное окружение (Python 3.11):

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

2. Установи зависимости для разработки (включает runtime + pytest):

   ```bash
   pip install -r requirements-dev.txt
   ```

3. Создай `.env` на основе примера:

   ```bash
   cp .env.example .env   # Windows: copy .env.example .env
   ```

   - `BOT_TOKEN` — токен от [@BotFather](https://t.me/BotFather) (обязателен).
   - `GEMINI_API_KEY` — бесплатный ключ с [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
     (без банковской карты). Опционален: без него бот работает, но
     персональные прогнозы используют заготовленный текст вместо AI.

4. Запусти бота:

   ```bash
   python main.py
   ```

## Запуск через Docker

```bash
docker compose up --build
```

Бот читает `BOT_TOKEN`/`GEMINI_API_KEY` из `.env` (секция `env_file` в
`docker-compose.yml`). SQLite-файл профилей сохраняется в `./data` на
хосте (volume), так что профили не теряются при пересборке контейнера.
Открытых портов не требуется — режим long polling.

## Тестирование

Тесты — обязательная часть процесса, не опция.

```bash
pip install -r requirements-dev.txt
pytest -v
```

Что покрыто тестами:

- **`test_horoscope.py`** / **`test_zodiac.py`** / **`test_categories.py`** —
  unit-тесты чистой логики: детерминизм, граничные значения знаков
  зодиака, уникальность кодов категорий.
- **`test_contracts.py`** — contract-тесты формата ответа. Покрывают как
  детерминированный `/horoscope`, так и конверт персонального сообщения
  (непустая строка, нужный заголовок, имя и категория внутри текста) —
  независимо от того, AI или фолбэк сгенерировал тело сообщения.
- **`test_storage.py`** — сохранение/чтение QA-профиля в SQLite (на
  временной БД, не трогает продовый файл).
- **`test_ai_advisor.py`** — сборка промпта и разбор ответа Gemini на
  поддельном клиенте (без реальных сетевых вызовов).
- **`test_handlers.py`** / **`test_handlers_profile.py`** /
  **`test_handlers_astro.py`** — хендлеры `/start`, FSM-шаги заполнения
  профиля и сценарий «категория → AI-прогноз → фолбэк при ошибке AI» —
  всё на лёгких заглушках `Message`/`CallbackQuery` и реальном
  `FSMContext` (без поднятия настоящего Bot/Dispatcher).
- **`test_config.py`** — загрузка и валидация конфигурации из окружения.

## QA Process — Definition of Done

Перед любым merge / push в `main`:

1. ✅ `pytest -v` — все тесты зелёные.
2. ✅ `docker build .` — образ собирается без ошибок.
3. ✅ Новая функциональность покрыта тестами (unit и/или contract).

Оба пункта 1 и 2 автоматически проверяются в CI
(`.github/workflows/ci.yml`) на каждый push и pull request в `main`.
PR с красным CI не должен мерджиться.

## Git flow

Простой trunk-based flow, дружелюбный к одиночной разработке и небольшой
команде:

- `main` — всегда в рабочем состоянии (тесты и docker build проходят).
- Новая работа — в отдельной ветке от `main`:
  - `feature/<короткое-описание>` — новая функциональность;
  - `fix/<короткое-описание>` — исправление бага;
  - `chore/<короткое-описание>` — рутина (зависимости, конфиги, CI).
- Коммиты — в стиле [Conventional Commits](https://www.conventionalcommits.org/):
  `feat: ...`, `fix: ...`, `test: ...`, `docs: ...`, `chore: ...`.

Типичный цикл:

```bash
git checkout main
git pull
git checkout -b feature/new-zodiac-signs

# ...вносим изменения...

pytest -v                              # 1. тесты должны быть зелёными
docker build -t qa-horoscope-bot .     # 2. образ должен собраться

git add <изменённые файлы>
git commit -m "feat: add five new QA zodiac signs"
git push -u origin feature/new-zodiac-signs
# открываем Pull Request в main, дожидаемся зелёного CI, мерджим
```

После мерджа ветку можно удалить: `git branch -d feature/new-zodiac-signs`.

## Как расширять бота

- **Новая категория астрорегрессии** — добавь `Category(...)` в
  [bot/categories.py](bot/categories.py). Клавиатура и AI-промпт подхватят
  её автоматически, ничего больше менять не нужно.
- **Новый уровень/специализация** — добавь пару `(code, label)` в
  [bot/profile_options.py](bot/profile_options.py).
- **Новые предсказания / советы / знаки для `/horoscope`** — добавь строку
  в `PREDICTIONS`, `ADVICE` или `QA_SIGNS` в [bot/horoscope.py](bot/horoscope.py).
- **Новая команда** — добавь хендлер в [bot/handlers.py](bot/handlers.py)
  (или новый файл `bot/handlers_*.py` + `dispatcher.include_router(...)`
  в [main.py](main.py)) и тест рядом.
- **Другая модель Gemini / другой AI-провайдер** — вся интеграция с AI
  изолирована в [bot/ai_advisor.py](bot/ai_advisor.py); поменяй там
  `MODEL_NAME`/клиент, контракт ответа (`bot/contracts.py`) и хендлеры
  не заметят разницы.
