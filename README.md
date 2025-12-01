# Shelter API

REST API для системы управления приютом животных. Построен на FastAPI, PostgreSQL и SQLAlchemy.

## Технологии

- **FastAPI** - веб-фреймворк
- **PostgreSQL** - база данных
- **SQLAlchemy** - ORM
- **Alembic** - миграции БД
- **JWT** - аутентификация (токены хранятся в PostgreSQL)
- **BCrypt** - хеширование паролей

## Установка

### Требования

- Python 3.8+
- PostgreSQL 12+

### Шаги установки

1. Клонировать репозиторий

2. Создать виртуальное окружение и установить зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Создать базу данных PostgreSQL:
```sql
CREATE DATABASE shelter_db;
```

4. Скопировать .env.example в .env и настроить переменные окружения:
```bash
cp .env.example .env
```

5. Применить миграции:
```bash
alembic upgrade head
```

## Запуск

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API будет доступно по адресу: http://localhost:8000

Документация Swagger UI: http://localhost:8000/docs

## API Endpoints

### Аутентификация
- `POST /api/v1/auth/register` - Регистрация пользователя
- `POST /api/v1/auth/login` - Вход в систему
- `POST /api/v1/auth/logout` - Выход из системы

### Пользователи
- `GET /api/v1/users/me` - Получить профиль текущего пользователя
- `PUT /api/v1/users/me` - Обновить профиль
- `GET /api/v1/users/{user_id}` - Получить пользователя по ID

### Животные
- `GET /api/v1/animals/` - Список животных (с фильтрами)
- `GET /api/v1/animals/{animal_id}` - Получить животное по ID
- `POST /api/v1/animals/` - Создать животное (только админ)
- `PUT /api/v1/animals/{animal_id}` - Обновить животное (только админ)
- `DELETE /api/v1/animals/{animal_id}` - Удалить животное (только админ)

### Заявки на опекунство
- `GET /api/v1/applications/` - Список заявок (только админ)
- `GET /api/v1/applications/{application_id}` - Получить заявку по ID (только админ)
- `POST /api/v1/applications/` - Создать заявку
- `PUT /api/v1/applications/{application_id}` - Обновить заявку (только админ)
- `DELETE /api/v1/applications/{application_id}` - Удалить заявку (только админ)

### Избранное
- `GET /api/v1/favorites/` - Список избранных животных
- `POST /api/v1/favorites/` - Добавить в избранное
- `DELETE /api/v1/favorites/{favorite_id}` - Удалить из избранного
- `DELETE /api/v1/favorites/animal/{animal_id}` - Удалить из избранного по ID животного

## Структура проекта

```
ShelterAPI/
├── app/
│   ├── core/
│   │   ├── config.py          # Конфигурация
│   │   ├── database.py        # Подключение к БД
│   │   ├── deps.py            # Зависимости (аутентификация)
│   │   └── security.py        # JWT и хеширование
│   ├── models/                # Модели SQLAlchemy
│   │   ├── user.py
│   │   ├── animal.py
│   │   ├── application.py
│   │   ├── favorite.py
│   │   ├── token.py
│   │   ├── guardian.py
│   │   └── enclosure.py
│   ├── routers/               # API endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── animals.py
│   │   ├── applications.py
│   │   └── favorites.py
│   ├── schemas/               # Pydantic схемы
│   │   ├── user.py
│   │   ├── animal.py
│   │   ├── application.py
│   │   └── favorite.py
│   ├── services/              # Бизнес-логика
│   └── main.py                # Точка входа
├── alembic/                   # Миграции
├── .env                       # Переменные окружения
├── .env.example               # Пример настроек
├── requirements.txt           # Зависимости
└── README.md

```

## База данных

### Основные таблицы

- **users** - Пользователи системы
- **tokens** - JWT токены
- **animal** - Животные в приюте
- **guardian** - Опекуны
- **application** - Заявки на опекунство
- **favorite** - Избранные животные
- **enclosure** - Вольеры

## Аутентификация

API использует JWT токены для аутентификации. Токены хранятся в таблице PostgreSQL.

При авторизации используйте заголовок:
```
Authorization: Bearer <token>
```

## Роли пользователей

- **User** - обычный пользователь (просмотр животных, создание заявок, избранное)
- **Admin** - администратор (управление животными, заявками)
