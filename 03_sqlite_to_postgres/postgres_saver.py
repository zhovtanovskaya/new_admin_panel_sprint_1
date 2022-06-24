"""Подключение и запись в PostgreSQL."""

from contextlib import contextmanager

import psycopg2
from db_objects import DESTINATION_MAPPING, SQLiteData
from psycopg2.extensions import connection as pg_connection
from psycopg2.extras import RealDictCursor


def create_connection(dsl: dict) -> pg_connection:
    """Создать подключение к базе PostgreSQL.

    Args:
        dsl: Настройки подключения к базе данных.

    Returns:
        Подключение к PostgreSQL.
    """
    connection = psycopg2.connect(**dsl, cursor_factory=RealDictCursor)
    connection.set_session(autocommit=True)
    return connection


@contextmanager
def postgres_connection(dsl: dict):
    """Создает подключение к PostgreSQL, которое закроет на выходе.

    Args:
        dsl: Настройки подключения к базе данных.

    Yields:
        Подключение к PostgreSQL.
    """
    connection = create_connection(dsl)
    yield connection
    connection.close()


class PostgresSaver:
    """Класс, импортирующий SQLite-данные в PostgreSQL."""

    def __init__(self, connection: pg_connection):
        self.connection = connection

    def _compose_insert_sql(self, table_name: str, columns: tuple) -> str:
        """Создать SQL-выражение вставки строки в PostgreSQL.

        Args:
            table_name: Таблица, куда вставлять значения.
            columns: Столбцы таблицы table_name, которые полагается заполнить.

        Returns:
            Строка INSERT-запроса.
        """
        placeholders = ('%s',) * len(columns)
        sql = """
            INSERT INTO {table} ({columns})
            VALUES ({placeholders}) ON CONFLICT DO NOTHING;
        """.format(
            table=table_name,
            columns=', '.join(columns),
            placeholders=', '.join(placeholders))
        return sql

    def _execute_sql(self, sql: str, values: tuple) -> None:
        """Запустить SQL.

        Args:
            sql: SQL-выражение.
            values: Значения для вставки в SQL-выражение.

        Raises:
            psycopg2.Error: В случае ошибки при SQL-вызове.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, values)

    def save(self, obj: SQLiteData) -> None:
        """Копировать SQLite-объект в PostgreSQL-таблицу.

        Args:
            obj: Объектное представление строки SQLite-таблицы.
        """
        obj_type = type(obj)
        msg = '"{type}" нет в DESTINATION_MAPPING.'.format(type=obj_type)
        assert obj_type in DESTINATION_MAPPING, msg
        destinations = DESTINATION_MAPPING[obj_type]

        attribute_mapping = destinations['attribute_to_column']
        columns = []
        values = []
        for attr_name, col_name in attribute_mapping.items():
            value = getattr(obj, attr_name)
            if value:
                values.append(value)
                columns.append(col_name)

        table_name = destinations['destination_table']
        sql = self._compose_insert_sql(table_name, columns)
        self._execute_sql(sql, values)
