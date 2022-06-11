import uuid
from contextlib import contextmanager

import psycopg2
from db_objects import FilmWork, Person
from psycopg2.errors import UniqueViolation
from psycopg2.extensions import connection as PGConnection
from psycopg2.extras import DictCursor


def create_connection(dsl: dict):
    return psycopg2.connect(**dsl, cursor_factory=DictCursor)


@contextmanager
def postgres_connection(dsl: dict):
    connection = self.create_connection(dsl)
    yield connection
    connection.close()


class PostgresSaver:

    def __init__(self, connection: PGConnection):
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
                id, title, description, rating, type, created, modified
            )
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW());
        '''
        values = (
            film_work.id,
            film_work.title,
            film_work.description,
            film_work.rating,
            film_work.type,
        )
        self._execute_sql(sql, values)
