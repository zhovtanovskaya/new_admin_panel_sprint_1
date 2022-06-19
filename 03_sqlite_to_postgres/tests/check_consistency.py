import logging
import sqlite3

import dateutil.parser
import psycopg2
import settings
from db_objects import (DESTINATION_MAPPING, SOURCE_MAPPING, FilmWork, Genre,
                        GenreFilmWork, Person, PersonFilmWork)
from postgres_saver import postgres_connection
from psycopg2.extensions import connection as pg_connection
from sqlite_loader import SQLiteLoader, sqlite_connection

logger = logging.getLogger('root')


def check_consistency(sqlite_conn: sqlite3.Connection, pg_conn: pg_connection):
    sqlite_loader = SQLiteLoader(sqlite_conn)
    sources = (FilmWork, Person, PersonFilmWork, Genre, GenreFilmWork)
    for source in sources:
        table_name = SOURCE_MAPPING[source]
        for obj in sqlite_loader.load(source):
            sql = 'SELECT * FROM {table} WHERE id=%s;'.format(table=table_name)
            values = (obj.id,)
            with pg_conn.cursor() as cursor:
                cursor.execute(sql, values)

                attribute_mapping = DESTINATION_MAPPING[source]['attribute_to_column']
                row = cursor.fetchone()
                if row is None:
                    logger.error('Missing {table_name}.id = {id}.')
                else:
                    for attr, column in attribute_mapping.items():
                        sqlite_value = getattr(obj, attr, None)
                        pg_value = row[column]
                        if sqlite_value != pg_value:
                            msg = (
                                'SQLite value "{table_name}.{attr}" do not '
                                'match PostgreSQL value "{table_name}.{column}": '
                                '{sqlite_value} != {pg_value}. '
                                'In {table_name}.id = {id}.'
                            ).format(
                                table_name=table_name,
                                attr=attr,
                                column=column,
                                sqlite_value=sqlite_value,
                                pg_value=pg_value,
                                id=obj.id)
                            logger.error(msg)


if __name__ == '__main__':
    with sqlite_connection(settings.SQLITE_DB_NAME) as sqlite_conn:
        with postgres_connection(settings.POSTGRES_DB) as pg_conn:
            check_consistency(sqlite_conn, pg_conn)
