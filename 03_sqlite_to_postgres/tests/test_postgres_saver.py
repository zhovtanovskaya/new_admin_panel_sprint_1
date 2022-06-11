import uuid
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


class TestPostgresSaver(TestCase):

    def setUp(self):
        self.connection = create_connection(DSL)
        self.saver = PostgresSaver(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_save_person(self):
        person = Person(id=str(uuid.uuid4()), full_name='George Lucas')
        self.saver.save_person(person)

    def test_save_film_work(self):
        film_work = FilmWork(
            id=str(uuid.uuid4()), 
            title=' Star Wars: Episode IV - A New Hope',
            description='The Imperial Forces...',
            rating=8.6,
            type='movie',
            creation_date='2022-06-11',
        )
        self.saver.save_film_work(film_work)


if __name__ == '__main__':
    main()
