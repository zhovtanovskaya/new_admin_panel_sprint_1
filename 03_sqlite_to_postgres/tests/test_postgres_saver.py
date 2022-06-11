import uuid
from unittest import TestCase, main

from postgres_saver import PostgresSaver


class TestPostgresSaver(TestCase):

    def test(self):
        saver = PostgresSaver()
        saver.save_person(id=str(uuid.uuid4()), full_name='George Lucas')


if __name__ == '__main__':
    main()
