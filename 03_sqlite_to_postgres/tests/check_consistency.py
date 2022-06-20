import sqlite3
from contextlib import closing

import dateutil.parser
import psycopg2
import settings
from db_objects import (DESTINATION_MAPPING, SOURCE_MAPPING, FilmWork, Genre,
                        GenreFilmWork, Person, PersonFilmWork)
from postgres_saver import postgres_connection
from psycopg2.extensions import connection as pg_connection
from sqlite_loader import SQLiteLoader, sqlite_connection


def compare_content(sqlite_obj, pg_row, attribute_mapping):
    for attr, column in attribute_mapping.items():
        sqlite_value = getattr(sqlite_obj, attr, None)
        pg_value = pg_row[column]
        assert sqlite_value == pg_value, \
            (
                'Значение в SQLite "{table_name}.{attr}" не равно '
                'значению в PostgreSQL "{table_name}.{column}": '
                '{sqlite_value} != {pg_value}. '
                'Смотри {table_name}.id = {id}.'
            ).format(
                table_name=table_name,
                attr=attr,
                column=column,
                sqlite_value=sqlite_value,
                pg_value=pg_value,
                id=sqlite_obj.id)


def get_sqlite_table_size(table_name: str, connection: sqlite3.Connection):
    sql = 'SELECT count(*) FROM {table};'.format(table=table_name)
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        return tuple(cursor.fetchone())[0]


def get_pg_table_size(table_name: str, connection: pg_connection):
    sql = 'SELECT count(*) FROM {table};'.format(table=table_name)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count']


def check_consistency(
        sqlite_conn: sqlite3.Connection, pg_conn: pg_connection):
    """Сравнить таблицы SQLite и PostgreSQL размерами и построчно.

    Args:
        sqlite_conn: Подключение к SQLite.
        pg_conn: Подключение к PostgreSQL.
    """
    tables = SOURCE_MAPPING.values()
    # Сравнить размеры таблиц.
    for table_name in tables:
        sqlite_table_size = get_sqlite_table_size(table_name, sqlite_conn)
        pg_table_size = get_pg_table_size(table_name, pg_conn)
        msg = 'Размеры таблиц "{table}" не равны'.format(table=table_name)
        assert sqlite_table_size == pg_table_size, msg

    # Сравнить содержимое SQLite и PostgreSQL.
    sqlite_loader = SQLiteLoader(sqlite_conn)
    for source, table_name in SOURCE_MAPPING.items():
        for obj in sqlite_loader.load(source):
            sql = 'SELECT * FROM {table} WHERE id=%s;'.format(table=table_name)
            values = (obj.id,)
            with pg_conn.cursor() as cursor:
                cursor.execute(sql, values)
                row = cursor.fetchone()
                attribute_mapping = DESTINATION_MAPPING[source][
                    'attribute_to_column']
                compare_content(obj, row, attribute_mapping)


if __name__ == '__main__':
    with sqlite_connection(settings.SQLITE_DB_NAME) as sqlite_conn:
        with postgres_connection(settings.POSTGRES_DB) as pg_conn:
            check_consistency(sqlite_conn, pg_conn)
