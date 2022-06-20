# Проектное задание: перенос данных

Вооружитесь библиотеками psycopg2 и sqlite3, чтобы создать скрипт для миграции данных в новую базу.

Критерии готовности:

- После применения скрипта все фильмы, персоны и жанры появляются в PostgreSQL.  
- Все связи между записями сохранены. 
- В коде используются `dataclass`.
- Данные загружаются пачками по n записей.
- Повторный запуск скрипта не создаёт дублирующиеся записи.
- В коде есть обработка ошибок записи и чтения.

# Настройка окружения

Прежде чем запускать команды, установите значение переменным окружения в
своем файле `03_sqlite_to_postgres/.env`. Создайте пустой `.env` через
копирование:

```
cd 03_sqlite_to_postgres/
cp .env.example .env
```

Затем впишите в него свои параметры подключения к базам данных.

# Команды

Запустить перенос данных из SQLite в PostgreSQL и проверить его:

```
cd 03_sqlite_to_postgres/
python ./load_data.py
python -m tests.check_consistency
```

# Unit-тесты

```
cd 03_sqlite_to_postgres/
. ./.env
cp db.sqlite $SQLITE_TEST_DB_NAME     # Создать базу для тестов.
# Создать схему в тестовой PostgreSQL.
psql -h $POSTGRES_TEST_DB_HOST -p $POSTGRES_TEST_DB_PORT -U $POSTGRES_TEST_DB_USER -d $POSTGRES_TEST_DB_NAME < ../01_schema_design/create_schema.ddl
```

Запуск тестов:

Выполнить unit-тесты:

```
python -m unit_tests.test_db_objects
python -m unit_tests.test_postgres_saver
python -m unit_tests.test_sqlite_loader
```
