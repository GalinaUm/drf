# DRF Project

## 📌 Описание проекта

Backend-приложение на Django REST Framework.

В проекте реализованы:
- работа с пользователями
- работа с материалами
- JWT-аутентификация
- фоновые задачи через Celery
- периодические задачи через Celery Beat

Стек:
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker / Docker Compose

---

## 🚀 Запуск проекта

### 1. Создать файл .env

Скопируйте файл `.env.sample` в `.env` и при необходимости измените значения.

Linux / Mac:
    cp .env.sample .env

Windows (PowerShell):
    copy .env.sample .env

---

### 2. Запустить проект

    docker compose up --build

---

## 🌐 Доступ к сервисам

После запуска:

- Backend: http://localhost:8000
- Swagger: http://localhost:8000/swagger/
- Redoc: http://localhost:8000/redoc/

---

## 🧩 Сервисы

Проект запускает:

- backend — Django приложение
- db — PostgreSQL
- redis — брокер сообщений
- celery — воркер фоновых задач
- celery-beat — планировщик задач

---

## 🔍 Проверка Celery

Логи воркера:
    docker compose logs celery

Логи планировщика:
    docker compose logs celery-beat

---

## 🛑 Остановка проекта

    docker compose down

---

## 🧹 Полная очистка (с удалением данных)

    docker compose down -v

---

## ⚙️ Переменные окружения

Все чувствительные данные вынесены в `.env`.

Пример:

    NAME=
    USER=
    PASSWORD=
    HOST=
    PORT=

    REDIS_HOST=
    REDIS_PORT=
    REDIS_PASSWORD=

---

## 📁 Структура проекта

    drf_project/
    ├── config/
    ├── users/
    ├── materials/
    ├── Dockerfile
    ├── docker-compose.yaml
    ├── .env.sample
    ├── manage.py

---

## 🧠 Важно

В Docker:
- PostgreSQL доступен по хосту `db`
- Redis доступен по хосту `redis`

Использование `localhost` внутри контейнеров не работает.