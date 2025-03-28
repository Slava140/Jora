#!/bin/sh

echo "Применение миграции"
alembic upgrade head

echo "Запуск приложения"
export FLASK_DEBUG=$APP_DEBUG
python -m flask --app src.main run --host $APP_HOST --port $APP_PORT

exec "$@"
