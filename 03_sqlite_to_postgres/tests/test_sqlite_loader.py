from unittest import TestCase, main

from sqlite_loader import SQLiteLoader


class TestStringMethods(TestCase):

    def test_load_film_works(self):
        loader = SQLiteLoader()
        data = loader.load_film_works()
        record = next(data)
        first_id = '3d825f60-9fff-4dfe-b294-1a45fa1e115d'
        self.assertEqual(first_id, record['id'])


if __name__ == '__main__':
    main()