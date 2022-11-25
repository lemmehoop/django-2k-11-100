# django 2k 11-100

- `python3 -m venv .venv` - создание виртуального окружения
- `source ./.venv/bin/activate` - вход в виртуальное окружение
- `docker-compose up -d` - поднять PostgreSQL с помощью Docker
- `pip install -r requirements.txt` - установка зависимостей
- `python src/manage.py migrate` - выполнить миграции
- `python src/manage.py runserver` - запуск сервера для разработки на http://localhost:8000
- `pytest` - запустить автоматические тесты
