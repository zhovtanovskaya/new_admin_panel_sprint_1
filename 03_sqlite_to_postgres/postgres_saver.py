import uuid
from contextlib import contextmanager

import psycopg2
from psycopg2.errors import UniqueViolation
from psycopg2.extras import DictCursor


@contextmanager
def postgres_connection(dsl: dict):
    connection = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield connection
    connection.close()


class PostgresSaver:

    def __init__(self, connection: psycopg2.extensions.connection):
        self.connection = connection
    
    def save_person(self, id: uuid, full_name: str):
        with self.connection.cursor() as cursor:
            sql = 'INSERT INTO person(id, full_name) VALUES (%s, %s);'
            values = (id, full_name)
            try:
                cursor.execute(sql, values)
            except UniqueViolation as e:
                print(e)
            self.connection.commit()