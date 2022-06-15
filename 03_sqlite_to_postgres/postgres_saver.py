"""Подключение и запись в PostgreSQL."""

from contextlib import contextmanager

import psycopg2
from db_objects import DESTINATION_MAPPING
from psycopg2.extensions import connection as pg_connection
from psycopg2.extras import RealDictCursor


def create_connection(dsl: dict):
    """Создать подключение к базе PostgreSQL.

    Args:
        dsl -- настройки подключения к базе данных.
    """
    return psycopg2.connect(**dsl, cursor_factory=RealDictCursor)


@contextmanager
def postgres_connection(dsl: dict):
    """Создает подключение к PostgreSQL, которое закроет на выходе.

    Args:
        dsl -- настройки подключения к базе данных.
    """
    connection = create_connection(dsl)
    yield connection
    connection.close()


class PostgresSaver:
    def __init__(self, connection: pg_connection):
        self.connection = connection

    def _compose_insert_sql(self, table_name, columns):
        placeholders = ('%s',) * len(columns)
        sql = '''
            INSERT INTO {table} ({columns})
            VALUES ({placeholders}) ON CONFLICT DO NOTHING;
        '''.format(
            table=table_name, 
            columns=', '.join(columns), 
            placeholders=', '.join(placeholders))
        return sql

    def _execute_sql(self, sql: str, values: tuple):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(sql, values)
            except psycopg2.Error as e:
                # Откатить транзакцию, чтобы избежать исключения 
                # InFailedSqlTransaction("current transaction is 
                # aborted, commands ignored until end of transaction block")
                # при следующем вызове cursor.execute().
                self.connection.rollback()
                raise e
            else:
                self.connection.commit()

    def save(self, obj):
        obj_type = type(obj)
        assert obj_type in DESTINATION_MAPPING, \
            '"{type}" нет в DESTINATION_MAPPING.'.format(type=obj_type)
        destinations = DESTINATION_MAPPING[obj_type]
        
        attribute_mapping = destinations['attribute_to_column']
        columns = []
        values = []
        for attr_name, col_name in attribute_mapping.items():
            value = getattr(obj, attr_name)
            if value:
                values.append(value)
                columns.append(col_name)

        table_name = destinations['destination_table']
        sql = self._compose_insert_sql(table_name, columns)
        self._execute_sql(sql, values)
