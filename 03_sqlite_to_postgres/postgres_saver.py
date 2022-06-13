"""Подключение и запись в PostgreSQL."""

from contextlib import contextmanager

import psycopg2
from db_objects import FilmWork, Person
from psycopg2.errors import UniqueViolation
from psycopg2.extensions import connection as pg_connection
from psycopg2.extras import RealDictCursor


def create_connection(dsl: dict):
    """Создать подключение к базе PostgreSQL.

    Args:
        dsl -- настройки подключения к базе данных.
    """
    return psycopg2.connect(**dsl, cursor_factory=RealDictCursor)


@contextmanager
def postgres_connection(dsl: dict):
    """Создает подключение к PostgreSQL, которое закроет на выходе.

    Args:
        dsl -- настройки подключения к базе данных.
    """
    connection = create_connection(dsl)
    yield connection
    connection.close()


class PostgresSaver:
    def __init__(self, connection: pg_connection):
        self.connection = connection

    def _execute_sql(self, sql: str, values: tuple):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(sql, values)
            except UniqueViolation as e:
                print(e)
            self.connection.commit()

    def save_person(self, person: Person):
        sql = '''
            INSERT INTO person (id, full_name, created, modified)
            VALUES (%s, %s, NOW(), NOW());
        '''
        values = (person.id, person.full_name)
        self._execute_sql(sql, values)

    def save_film_work(self, film_work: FilmWork):
        sql = '''
            INSERT INTO film_work (
                id,
                title,
                description,
                rating,
                type,
                creation_date,
                created,
                modified
            )
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW());
        '''
        values = (
            film_work.id,
            film_work.title,
            film_work.description,
            film_work.rating,
            film_work.type,
            film_work.creation_date,
        )
        self._execute_sql(sql, values)
