import sqlite3
from contextlib import contextmanager

from db_objects import SOURCE_MAPPING, FilmWork, Person


def create_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def sqlite_connection(db_path: str):
    connection = create_connection(db_path)
    yield create_connection(db_path)
    connection.close()


class SQLiteLoader:
    """Загрузчик содержимого таблиц SQLite."""

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def _load_data(self, TableDataClass):
        table_name = SOURCE_MAPPING[TableDataClass]
        curs = self.connection.cursor()
        curs.execute('SELECT * FROM {table};'.format(table=table_name))
        data = curs.fetchall()
        for row in data:
            row_dict = dict(zip(row.keys(), tuple(row)))
            obj = TableDataClass(**row_dict)
            yield obj

    def load_film_works(self):
        return self._load_data(FilmWork)

    def load_persons(self):
        return self._load_data(Person)

