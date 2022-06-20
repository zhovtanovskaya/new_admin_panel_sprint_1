from datetime import datetime
from unittest import TestCase, main

from db_objects import FilmWork


class TestFilmWork(TestCase):

    def setUp(self):
        self.film_work = FilmWork(
            title=' Star Wars: Episode IV - A New Hope',
            description='The Imperial Forces...',
            type='movie',
            creation_date='2021-06-16',
            created_at='2021-06-16 20:14:09.313086+00',
            updated_at='2021-06-16 20:14:09.313086+00',
        )

    def test_created_at_is_datetime(self):
        self.assertEqual(datetime, type(self.film_work.created_at))

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(self.film_work.updated_at))


if __name__ == '__main__':
    main()
