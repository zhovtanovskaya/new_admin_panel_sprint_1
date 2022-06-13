"""Основной модуль для импорта кино из SQLite в PostgreSQL."""

import os
import sqlite3

from dotenv import load_dotenv
from postgres_saver import PostgresSaver, postgres_connection
from psycopg2.extensions import connection as pg_connection
from sqlite_loader import SQLiteLoader, sqlite_connection

load_dotenv()


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: pg_connection):
    """Основной метод загрузки данных из SQLite в Postgres.

    Args:
        sqlite_conn: подключение к базе источкику данных SQLite.
        pg_conn: подключение к базе приемнику данных в PostgreSQL.
    """
    loader = SQLiteLoader(sqlite_conn)
    saver = PostgresSaver(pg_conn)
    with pg_conn.cursor() as curs:
        curs.execute('TRUNCATE person CASCADE;')
    pg_conn.commit()

    for obj in loader.load_persons():
        saver.save_person(obj)
        print(obj.id)
        break
    for obj in loader.load_film_works():
        saver.save_film_work(obj)
        print(obj.id)
        break


if __name__ == '__main__':
    dsl = {
        'dbname': os.getenv('POSTGRES_DB_NAME'),
        'user': os.getenv('POSTGRES_DB_USER'),
        'password': os.getenv('POSTGRES_DB_PASSWORD'),
        'host': '127.0.0.1',
        'port': 5432,
    }
    sqlite_db_name = os.getenv('SQLITE_DB_NAME')
    with sqlite_connection(sqlite_db_name) as sqlite_conn:
        with postgres_connection(dsl) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
