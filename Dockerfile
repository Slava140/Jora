FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN apk add curl postgresql-dev

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /jora/

COPY . .

RUN poetry install --no-interaction

WORKDIR ./src/

CMD ["python", "main.py"]