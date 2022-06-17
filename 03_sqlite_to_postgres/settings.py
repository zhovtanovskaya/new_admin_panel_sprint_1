import os

from dotenv import load_dotenv

load_dotenv()


SQLITE_DB_NAME = os.getenv('SQLITE_DB_NAME')
POSTGRES_DB = {
    'dbname': os.getenv('POSTGRES_DB_NAME'),
    'user': os.getenv('POSTGRES_DB_USER'),
    'password': os.getenv('POSTGRES_DB_PASSWORD'),
    'host': '127.0.0.1',
    'port': 5432,
}

SQLITE_TEST_DB_NAME = 'db.sqlite'
POSTGRES_TEST_DB = {
    'dbname': os.getenv('POSTGRES_DB_NAME'),
    'user': os.getenv('POSTGRES_DB_USER'),
    'password': os.getenv('POSTGRES_DB_PASSWORD'),
    'host': '127.0.0.1',
    'port': 5432,
}
