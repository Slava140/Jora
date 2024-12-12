#!/bin/sh

echo "Применение миграции"
alembic upgrade 0

echo "Запуск приложения"
python src/main.py

exec "$@"
