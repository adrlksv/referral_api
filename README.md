# Реферальная система API

Это проект по разработке простого RESTful API для реферальной системы. API позволяет пользователям регистрироваться, аутентифицироваться, создавать и удалять реферальные коды, а также использовать реферальные коды для регистрации.

## Требования
- Python 3.10.11
- PostgreSQL
- Redis
- Alembic

## Установка

1. Клонируйте репозиторий:

```
git clone https://github.com/ваш-репозиторий
cd referral_api
```

2. Установите зависимости:
```
python -m pip install -r requirements.txt
```

3. Создайте файл **.env** в корне проекта с настройками базы данных и других параметров. Пример:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=referral_db
DB_PASS=postgres
DB_USER=postgres

SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=HS256

GITHUB_CLIENT_ID=ваш_github_client_id
GITHUB_CLIENT_SECRET=ваш_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:8000/oauth/github/callback
GITHUB_AUTH_URL=https://github.com/login/oauth/authorize
GITHUB_TOKEN_URL=https://github.com/login/oauth/access_token
GITHUB_USER_URL=https://api.github.com/user

REDIS_HOST=localhost
REDIS_PORT=6379
``` 

4. Запустите миграции базы данных с помощью Alembic:
```
alembic upgrade head
```

5. Запустите приложение:
```
uvicorn src.main:app --reload
```
Приложение будет доступно по адресу **http://localhost:8000**

## Документация API
Документация доступна через Swagger UI (http://localhost:8000/docs) или ReDoc (http://localhost:8000/redoc)

## Основные эндпоинты
### Регистрация и аунтефикация
- POST /auth/register: Регистрация нового пользователя.
- POST /auth/login: Вход пользователя по email и паролю.
- POST /auth/logout: Выход пользователя, удаление токенов.
- POST /auth/refresh: Обновление access токена по refresh токену.
- GET /auth/me: Получение информации о текущем пользователе.
- GET /oauth/github/login: Регистрация/вход через GitHub (нужно перейти по этому пути, не через Swagger)
- GET /oauth/github/callback: Завершение процесса OAuth-аунтефикации, получение информации о пользователе, получение токена

## Кеширование
Для кеширования используется Redis. Все данные о реферальных кодах кэшируются в памяти.

## Тестирование
Для тестирования API можно использовать Swagger UI (http://localhost:8000/docs). Пример:
1. Зарегистрируйтесь через эндпоинт **/auth/register**.
2. Выполните вход через **/auth/login** и получите токены.
3. Создайте реферальный код через **/referral/create**.
