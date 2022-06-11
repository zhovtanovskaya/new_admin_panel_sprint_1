from unittest import TestCase, main

from sqlite_loader import SQLiteLoader


class TestStringMethods(TestCase):

    def setUp(self):
        self.loader = loader = SQLiteLoader()

    def test_load_film_works(self):
        data = self.loader.load_film_works()
        record = next(data)
        self.assertEqual('Star Wars: Episode IV - A New Hope', record.title)

    def test_load_persons(self):
        data = self.loader.load_persons()
        record = next(data)
        self.assertEqual('George Lucas', record.full_name)


if __name__ == '__main__':
    main()