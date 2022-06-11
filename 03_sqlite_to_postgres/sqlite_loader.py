import sqlite3
from contextlib import contextmanager


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


class SQLiteLoader:

    db_path = 'db.sqlite'
    KNOWN_TABLES = (
        'film_work',
        'person',
        'genre',
        'genre_film_work',
        'person_film_work',
    )

    def _load_data(self, table_name):
        error = 'Unknown table {table}".'.format(table=table_name)
        assert table_name in self.KNOWN_TABLES, error
        with conn_context(self.db_path) as conn:
            curs = conn.cursor()
            curs.execute("SELECT * FROM {table};".format(table=table_name))
            data = curs.fetchall()
            for row in data:
                yield dict(zip(row.keys(), tuple(row)))        

    def load_film_works(self):
        table_name = 'film_work'
        return self._load_data(table_name)

    def load_persons(self):
        table_name = 'person'
        return self._load_data(table_name)

    def load_genres(self):
        table_name = 'genre'
        return self._load_data(table_name)
