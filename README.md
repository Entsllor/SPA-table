# SPA-table

> Тестовое задание на позицию web-программист (Python)

Таблица содержит 4 колонки:
- Дата
- Название
- Количество
- Расстояние

Стек:
- База данных: PostgreSQL
- Backend: FastAPI
- Frontend: React

Таблица имеет сортировку по всем полям кроме даты (согласно ТЗ). 
Фильтрация в виде двух выпадающих списков и текстового поля:
- Выбор колонки, по которой будет фильтрация
- Выбор условия (равно, содержит, больше, меньше)
- Поле для ввода значения для фильтрации
- Таблица должна содержать пагинацию

Вся таблица должна работать без перезагрузки страницы.

# Pre-requirements

Перед запуском проекта необходимо установить переменные окружения
в файле backend/app/.env

```dotenv
# backend/app/.env
APP_DB_URL=postgresql+asyncpg://POSTGRES_USER:POSTGRES_PASSWORD@postgres:5432/POSTGRES_DB
APP_SECRET_KEY=YOUR-SECRET-KEY
```

Порт "postgres" указывается в случае запуска проекта через docker-compose,
в другом случае можно использовать localhost.

В docker-compose.yml необходимо прописать соответствующие POSTGRES_DBб POSTGRES_PASSWORD, POSTGRES_USER
