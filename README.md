# todo_bot

Простой Telegram ToDo-бот на `aiogram 3`: пользователь добавляет задачи командой `/add`, смотрит список через `/tsk`, а завершение задачи происходит кликом по inline-кнопке.

## Возможности

- регистрация пользователя командой `/start`;
- добавление задачи через `/add`;
- просмотр активных задач через `/tsk`;
- завершение задачи кликом по кнопке;
- хранение пользователей и задач в PostgreSQL;
- миграции схемы через Alembic;
- базовые async-тесты для CRUD, клавиатуры и конфигурации.

## Стек

- Python 3.10+;
- aiogram 3;
- SQLAlchemy 2 async;
- PostgreSQL;
- Alembic;
- pytest + pytest-asyncio.

## Быстрый запуск

```bash
git clone https://github.com/DenisKadyrov/todo_bot.git
cd todo_bot

python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

cp .env.example .env
```

Откройте `.env` и вставьте токен Telegram-бота в `BOT_TOKEN`. Токен можно получить у BotFather.

```bash
docker compose up -d
alembic upgrade head
python bot.py
```

Если установлен `make`, можно использовать короткие команды:

```bash
make db-up
make migrate
make run
```

## Переменные окружения

```env
BOT_TOKEN=telegram_bot_token

POSTGRES_SERVER=localhost
POSTGRES_USER=admin
POSTGRES_PASSWORD=Passw0rd
POSTGRES_DB=tasks
POSTGRES_PORT=5433
```

`SQLALCHEMY_DATABASE_URI` можно не задавать: приложение соберет строку подключения из переменных `POSTGRES_*`. Если переменная `SQLALCHEMY_DATABASE_URI` задана явно, она будет использована вместо собранной строки.

## Миграции

Применить миграции:

```bash
alembic upgrade head
```

Создать новую миграцию после изменения моделей:

```bash
alembic revision --autogenerate -m "describe change"
```

Перед коммитом новой миграции проверьте, что она не содержит лишних изменений и применима на чистую базу.

## Тесты

Запуск тестов:

```bash
pytest
```

Тесты используют временную SQLite-базу через async SQLAlchemy, поэтому для базовых проверок не нужен запущенный PostgreSQL. Для проверки миграций все еще нужен PostgreSQL из `docker compose`.

## Структура проекта

- `bot.py` - точка входа, создание бота, диспетчера и подключения к базе;
- `handlers.py` - обработчики команд и callback-запросов;
- `crud.py` - операции чтения/записи для моделей;
- `models/` - SQLAlchemy-модели;
- `schemas/` - Pydantic-схемы входных данных;
- `middlewares/` - middleware для передачи DB-сессии в handlers;
- `keybroads/` - построение inline-клавиатур;
- `migration/` - Alembic-миграции;
- `tests/` - тесты проекта.

## Полезные команды

```bash
docker compose ps
docker compose logs postgres
docker compose down
pytest
```

Для полного удаления локальной базы:

```bash
docker compose down -v
```
