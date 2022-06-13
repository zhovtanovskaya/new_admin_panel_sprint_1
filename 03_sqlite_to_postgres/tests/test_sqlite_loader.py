from unittest import TestCase, main

from db_objects import FilmWork, Person
from sqlite_loader import SQLiteLoader, create_connection

DB_PATH = 'db.sqlite'


class TestSQLiteLoader(TestCase):
    def setUp(self):
        self.connection = create_connection(DB_PATH)
        self.loader = SQLiteLoader(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_load_film_works(self):
        data = self.loader.load(FilmWork)
        record = next(data)
        self.assertEqual('Star Wars: Episode IV - A New Hope', record.title)

    def test_load_persons(self):
        data = self.loader.load(Person)
        record = next(data)
        self.assertEqual('George Lucas', record.full_name)


if __name__ == '__main__':
    main()
