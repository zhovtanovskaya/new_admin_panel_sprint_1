# Проектное задание: перенос данных

Вооружитесь библиотеками psycopg2 и sqlite3, чтобы создать скрипт для миграции данных в новую базу.

Критерии готовности:

- После применения скрипта все фильмы, персоны и жанры появляются в PostgreSQL.  
- Все связи между записями сохранены. 
- В коде используются `dataclass`.
- Данные загружаются пачками по n записей.
- Повторный запуск скрипта не создаёт дублирующиеся записи.
- В коде есть обработка ошибок записи и чтения.

# Команды

Запустить перенос данных из SQLite в PostgreSQL и проверить его:

```
cd 03_sqlite_to_postgres/
python ./load_data.py
python -m tests.check_consistency
```

Выполнить unit-тесты:

```
python -m unit_tests.test_db_objects
python -m unit_tests.test_postgres_saver
python -m unit_tests.test_sqlite_loader
```
