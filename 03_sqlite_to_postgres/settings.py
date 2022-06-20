import os

from dotenv import load_dotenv

load_dotenv()


SQLITE_DB_NAME = os.getenv('SQLITE_DB_NAME')
POSTGRES_DB = {
    'dbname': os.getenv('POSTGRES_DB_NAME'),
    'user': os.getenv('POSTGRES_DB_USER'),
    'password': os.getenv('POSTGRES_DB_PASSWORD'),
    'host': os.getenv('POSTGRES_DB_HOST'),
    'port': os.getenv('POSTGRES_DB_PORT'),
}

SQLITE_TEST_DB_NAME = os.getenv('SQLITE_TEST_DB_NAME')
POSTGRES_TEST_DB = {
    'dbname': os.getenv('POSTGRES_TEST_DB_NAME'),
    'user': os.getenv('POSTGRES_TEST_DB_USER'),
    'password': os.getenv('POSTGRES_TEST_DB_PASSWORD'),
    'host': os.getenv('POSTGRES_TEST_DB_HOST'),
    'port': os.getenv('POSTGRES_TEST_DB_PORT'),
}
