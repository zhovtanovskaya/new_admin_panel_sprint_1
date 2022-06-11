import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field


@dataclass(frozen=True)
class FilmWork:
    title: str
    description: str
    file_path: str
    type: str
    creation_date: str
    created_at: str
    updated_at: str
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Person:
    full_name: str
    created_at: str
    updated_at: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


def create_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def sqlite_connection(db_path: str):
    yield create_connection(db_path)
    conn.close()


class SQLiteLoader:
    """Загрузчик содержимого таблиц SQLite."""

    KNOWN_TABLES = {
        'film_work': FilmWork,
        'person': Person,
        'genre': None,
        'genre_film_work': None,
        'person_film_work': None,
    }

    def __init__(self, connection):
        self.connection = connection

    def _load_data(self, table_name):
        error = 'Unknown table {table}".'.format(table=table_name)
        assert table_name in self.KNOWN_TABLES.keys(), error
        TableDataClass = self.KNOWN_TABLES[table_name]
        curs = self.connection.cursor()
        curs.execute("SELECT * FROM {table};".format(table=table_name))
        data = curs.fetchall()
        for row in data:
            row_dict = dict(zip(row.keys(), tuple(row)))
            obj = TableDataClass(**row_dict)
            yield obj

    def load_film_works(self):
        table_name = 'film_work'
        return self._load_data(table_name)

    def load_persons(self):
        table_name = 'person'
        return self._load_data(table_name)

    def load_genres(self):
        table_name = 'genre'
        return self._load_data(table_name)
