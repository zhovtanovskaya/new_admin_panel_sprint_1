"""Подключение и экспорт данных из SQLite."""

import sqlite3
from contextlib import closing, contextmanager

from db_objects import SOURCE_MAPPING, SQLiteData


def create_connection(db_path: str) -> sqlite3.Connection:
    """Создать подключение к SQLite.

    Args:
        db_path: Путь к файлу базы данных.

    Returns:
        Подключение к SQLite.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def sqlite_connection(db_path: str):
    """Создать подключение к SQLite.

    Args:
        db_path: Путь к файлу базы данных.

    Yields:
        Подключение к SQLite.
    """
    connection = create_connection(db_path)
    yield connection
    connection.close()


class SQLiteLoader:
    """Загрузчик содержимого таблиц SQLite."""

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def load(self, sqlite_data_class: type, fetch_size=10) -> SQLiteData:
        """Загрузить объекты таблицы SQLite.

        Args:
            sqlite_data_class: Тип объекта, отвечающих строке таблицы SQLite.
            fetch_size: Читать из таблицы по fetch_size строк.

        Yields:
            Объект типа sqlite_data_class, отвечающий одной строке таблицы.
        """
        table_name = SOURCE_MAPPING[sqlite_data_class]
        with closing(self.connection.cursor()) as curs:
            curs.execute('SELECT * FROM {table};'.format(table=table_name))
            while data := curs.fetchmany(fetch_size):
                for row in data:
                    row_dict = dict(zip(row.keys(), tuple(row)))
                    obj = sqlite_data_class(**row_dict)
                    yield obj
