## Описание проекта
Вставить

## Техно-стек
* python 3.10
* fastapi 0.78.0
* asyncpg 0.27.0
* sqlalchemy 1.4.36
* alembic 1.7.7
* uvicorn 0.17.6
* fastapi-pagination 0.9.1
* sqladmin 0.14.1
* postgres 15.1

## Запуск проекта
1. Клонировать репозиторий и перейти в него в командной строке
```
git clone git@github.com:avnosov3/Shops.git
cd Shops/
```

2. Создать .env и заполнить
```
DB_ENGINE=postgresql+asyncpg
POSTGRES_DB=shops
POSTGRES_USER=<Указать имя пользователя>
POSTGRES_PASSWORD=<Указать пароль пользователя>
DB_HOST=db
DB_PORT=5432
```
3. Запустить docker compose
```
docker compose up -d
```
4. Заполнить БД
```
отправить GET запрос на http://127.0.0.1/api/v1/autogenerate/
```

После запуска появится доступ к:
* [swagger](http://127.0.0.1/docs/)
* [redoc](http://127.0.0.1/redoc/)
* [Админке fastapi](http://127.0.0.1/admin/)
* [Админке postgres](http://127.0.0.1/adminer/)

## Запуск тестов

1. Клонировать репозиторий и перейти в него в командной строке
```
git clone git@github.com:avnosov3/Shops.git
cd Shops/
```

2. Создать .env и заполнить
```
DB_ENGINE=postgresql+asyncpg
POSTGRES_DB=shops
POSTGRES_USER=<Указать имя пользователя>
POSTGRES_PASSWORD=<Указать пароль пользователя>
DB_HOST=test-db
DB_PORT=5432
```
3. Запустить docker compose
```
docker compose -f tests-docker-compose.yml up --attach tests
```
