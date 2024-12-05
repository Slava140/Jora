#!/bin/sh
set -e

alembic stamp head

echo "Создание миграции."
alembic revision --autogenerate

echo "Применение миграции"
alembic upgrade head

echo "Запуск приложения"
python src/main.py

exec "$@"
