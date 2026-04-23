.PHONY: install db-up db-down migrate run test

install:
	pip install -r requirements.txt

db-up:
	docker compose up -d

db-down:
	docker compose down

migrate:
	alembic upgrade head

run:
	python bot.py

test:
	pytest
