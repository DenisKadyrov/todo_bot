# todo_bot

**RUN**
```
git clone https://github.com/DenisKadyrov/todo_bot.git
cd todo_bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker-compose up -d
alembic upgrade head
python bot.py
```
