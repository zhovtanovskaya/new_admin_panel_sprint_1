from contextlib import contextmanager

import psycopg2
# from psycopg2.errors import UniqueViolation
from psycopg2.extras import DictCursor

DSL = {
    'dbname': 'movies_database', 
    'user': 'app', 
    'password': '123qwe', 
    'host': '127.0.0.1', 
    'port': 5432,
}


@contextmanager
def postgres_connection(dsl: dict):
    connection = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield connection
    connection.close()


class PostgresSaver:
    
    def save(self):
        with postgres_connection(DSL) as connection:
            with connection.cursor() as cursor:
                sql = 'INSERT INTO person(id, full_name) VALUES (%s, %s);'
                values = ('3d825f60-9fff-4dfe-b294-1a45fa1e115d', 'George Lucas')
                cursor.execute(sql, values)
                cursor.execute('SELECT * FROM person;')
                for record in cursor:
                    print(record)
                connection.commit()