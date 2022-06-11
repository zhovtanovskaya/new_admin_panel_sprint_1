from unittest import TestCase, main

from postgres_saver import PostgresSaver


class TestPostgresSaver(TestCase):

    def test(self):
        saver = PostgresSaver()
        saver.save()


if __name__ == '__main__':
    main()
