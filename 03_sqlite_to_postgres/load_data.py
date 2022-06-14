"""Основной модуль для импорта кино из SQLite в PostgreSQL."""

import sqlite3

import settings
from db_objects import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from postgres_saver import PostgresSaver, postgres_connection
from psycopg2.extensions import connection as pg_connection
from sqlite_loader import SQLiteLoader, sqlite_connection


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
    with sqlite_connection(settings.SQLITE_DB_NAME) as sqlite_conn:
        with postgres_connection(settings.POSTGRES_DB) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
