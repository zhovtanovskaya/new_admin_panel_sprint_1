import uuid
from unittest import TestCase, main

from postgres_saver import PostgresSaver, postgres_connection

DSL = {
    'dbname': 'movies_database', 
    'user': 'app', 
    'password': '123qwe', 
    'host': '127.0.0.1', 
    'port': 5432,
}


class TestPostgresSaver(TestCase):

    def test(self):
        with postgres_connection(DSL) as connection:
            saver = PostgresSaver(connection)
            saver.save_person(id=str(uuid.uuid4()), full_name='George Lucas')


if __name__ == '__main__':
    main()
