# Jora

### Простой трекер задач.

---

## Установка

1. Клонируйте репозиторий.
   ```bash
   git clone https://github.com/Slava140/Jora.git
   ```

2. Измените файл `.env.example` и переименуйте в `.env`.

3. Поднимите docker-compose.
   ```bash
   docker-compose up -d --build
   ```

4. Выполнить **после первого запуска**. При последующих **не нужно**, данные сохраняются в `pg_data`.
   - Подключитесь к контейнеру `postgres`.
     ```bash
     docker exec -it postgres psql -U postgres
     ```
   - Создайте базу данных с названием, которое указали в `DB_NAME` в `.env`.
     ```sql
     CREATE DATABASE name;
     ```
   - Выйдите из контейнера
     ```bash
     exit
     ```
5. 
   