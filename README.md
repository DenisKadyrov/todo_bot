# todo_bot
Простой ToDo telegram бот на aiogram. Его основыне вунскции это добавление задач при помощи команды /add и вывод списка задач при помощи /tsk. Список выводиться в виде инлайн клавиатуры, при нажатии на который задача удаляеться из списка и считается выполненной.

**RUN**
```
git clone https://github.com/DenisKadyrov/todo_bot.git
cd todo_bot
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
docker-compose up -d
cp .env.example .env
vim .env
# Нужно в поле токена вставить токен тг бота
alembic upgrade head
python bot.py
```
