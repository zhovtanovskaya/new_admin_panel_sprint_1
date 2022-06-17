import sqlite3
from contextlib import closing, contextmanager

from db_objects import SOURCE_MAPPING, FilmWork, Person


def create_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def sqlite_connection(db_path: str):
    connection = create_connection(db_path)
    yield connection
    connection.close()


class SQLiteLoader:
    """Загрузчик содержимого таблиц SQLite."""

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def load(self, TableDataClass, fetch_size=10):
        table_name = SOURCE_MAPPING[TableDataClass]
        with closing(self.connection.cursor()) as curs:
            curs.execute('SELECT * FROM {table};'.format(table=table_name))
            data = curs.fetchmany(fetch_size)
            while data:
                for row in data:
                    row_dict = dict(zip(row.keys(), tuple(row)))
                    obj = TableDataClass(**row_dict)
                    yield obj
                data = curs.fetchmany(fetch_size)
