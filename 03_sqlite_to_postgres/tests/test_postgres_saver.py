import uuid
from datetime import datetime, timezone
from unittest import TestCase, main

from db_objects import FilmWork, Person
from postgres_saver import PostgresSaver, create_connection

DSL = {
    'dbname': 'movies_database',
    'user': 'app',
    'password': '123qwe',
    'host': '127.0.0.1',
    'port': 5432,
}


class PostgresTableTestCase(TestCase):

    table_name = ''

    def _truncate(self):
        with self.connection.cursor() as curs:
            curs.execute('TRUNCATE {table} CASCADE;'.format(table=self.table_name))
        self.connection.commit()

    def setUp(self):
        self.connection = create_connection(DSL)
        self._truncate()

    def fetchall(self):
        with self.connection.cursor() as curs:
            curs.execute('SELECT * FROM {table};'.format(table=self.table_name))
            return curs.fetchall()

    def tearDown(self):
        self._truncate()
        self.connection.close()


class TestPostgresSaverSavePerson(PostgresTableTestCase):

    table_name = 'person'

    def setUp(self):
        super().setUp()
        saver = PostgresSaver(self.connection)
        self.data = {
            'id': str(uuid.uuid4()),
            'full_name': 'George Lucas',
        }
        person = Person(**self.data)
        saver.save(person)

    def test_data_in_columns(self):
        row = self.fetchall()[0]
        for key in self.data.keys():
            self.assertEqual(self.data[key], row.get(key))

    def test_created_one_row(self):
        rows = self.fetchall()
        self.assertEqual(1, len(rows))


class TestPostgresSaverSaveFilmWork(PostgresTableTestCase):

    table_name = 'film_work'

    def setUp(self):
        super().setUp()
        saver = PostgresSaver(self.connection)
        self.data = {
            'id': str(uuid.uuid4()),
            'title': ' Star Wars: Episode IV - A New Hope',
            'description': 'The Imperial Forces...',
            'rating': 8.6,
            'type': 'movie',
            'creation_date': datetime(2022, 6, 11).date(),
            
        }
        self.created_at = datetime(2022, 6, 11, tzinfo=timezone.utc)
        self.updated_at = datetime(2022, 6, 11, tzinfo=timezone.utc)
        film_work = FilmWork(
            **self.data, 
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        saver.save(film_work)

    def test_data_in_columns(self):
        row = self.fetchall()[0]
        for key in self.data.keys():
            self.assertEqual(self.data[key], row.get(key))
        self.assertEqual(self.created_at, row.get('created'))
        self.assertEqual(self.updated_at, row.get('modified'))

    def test_created_one_row(self):
        rows = self.fetchall()
        self.assertEqual(1, len(rows))


if __name__ == '__main__':
    main()
