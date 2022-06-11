import sqlite3

import psycopg2
from postgres_saver import PostgresSaver, postgres_connection
from psycopg2.extensions import connection as PGConnection
from psycopg2.extras import DictCursor
from sqlite_loader import SQLiteLoader, sqlite_connection


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: PGConnection):
    """Основной метод загрузки данных из SQLite в Postgres."""

    loader = SQLiteLoader(sqlite_conn)
    saver = PostgresSaver(pg_conn)
    with pg_conn.cursor() as curs:
        curs.execute('TRUNCATE person CASCADE;')
    pg_conn.commit()
    for obj in loader.load_persons():
        saver.save_person(obj.id, obj.full_name)
        print(obj.id)

if __name__ == '__main__':
    dsl = {
        'dbname': 'movies_database', 
        'user': 'app', 
        'password': '123qwe', 
        'host': '127.0.0.1', 
        'port': 5432,
    }
    sqlite_db_name = 'db.sqlite'
    with sqlite_connection(sqlite_db_name) as sqlite_conn:
        with postgres_connection(dsl) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
