import uuid
from unittest import TestCase, main

from db_objects import FilmWork, Person
from postgres_saver import PostgresSaver, postgres_connection

DSL = {
    'dbname': 'movies_database', 
    'user': 'app', 
    'password': '123qwe', 
    'host': '127.0.0.1', 
    'port': 5432,
}


class TestPostgresSaver(TestCase):

    def test_save_person(self):
        with postgres_connection(DSL) as connection:
            saver = PostgresSaver(connection)
            person = Person(id=str(uuid.uuid4()), full_name='George Lucas')
            saver.save_person(person)

    def test_save_film_work(self):
        with postgres_connection(DSL) as connection:
            saver = PostgresSaver(connection)
            film_work = FilmWork(
                id=str(uuid.uuid4()), 
                title=' Star Wars: Episode IV - A New Hope',
                description='The Imperial Forces...',
                rating=8.6,
                type='movie',
                creation_date='2022-06-11',
            )
            saver.save_film_work(film_work)


if __name__ == '__main__':
    main()
