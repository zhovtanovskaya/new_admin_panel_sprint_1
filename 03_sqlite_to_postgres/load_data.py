"""Основной модуль для импорта кино из SQLite в PostgreSQL."""

import logging
import sqlite3

import settings
from db_objects import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from postgres_saver import PostgresSaver, postgres_connection
from psycopg2.errors import ForeignKeyViolation
from psycopg2.extensions import connection as pg_connection
from sqlite_loader import SQLiteLoader, sqlite_connection

logger = logging.getLogger('root')


def load_from_sqlite(
        sqlite_conn: sqlite3.Connection, pg_conn: pg_connection) -> None:
    """Основной метод загрузки данных из SQLite в Postgres.

    Args:
        sqlite_conn: подключение к базе источкику данных SQLite.
        pg_conn: подключение к базе приемнику данных в PostgreSQL.
    """
    loader = SQLiteLoader(sqlite_conn)
    saver = PostgresSaver(pg_conn)

    sources = (FilmWork, Person, PersonFilmWork, Genre, GenreFilmWork)
    for source in sources:
        for obj in loader.load(source):
            try:
                saver.save(obj)
            except ForeignKeyViolation as e:
                logger.error(e)
            except Exception as e:
                msg = 'Failed to save {type} id={id}.'.format(
                    type=type(obj), id=obj.id)
                logger.error(msg)
                logger.exception(e)
            else:
                msg = 'Imported {type} id={id}.'.format(
                    type=type(obj), id=obj.id)
                logger.debug(msg)


if __name__ == '__main__':
    with (
        sqlite_connection(settings.SQLITE_DB_NAME) as sqlite_conn,
        postgres_connection(settings.POSTGRES_DB) as pg_conn,
    ):
            load_from_sqlite(sqlite_conn, pg_conn)
