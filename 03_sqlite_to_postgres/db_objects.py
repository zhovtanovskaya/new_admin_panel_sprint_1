"""Python-представление данных, импортируемых из SQLite."""

import uuid
from dataclasses import dataclass, field, fields
from datetime import datetime

from dateutil.parser import parse


class SQLiteData:
    """Базовый класс для объектного представления таблиц SQLite."""

    def __post_init__(self):
        """Сделать изменения после инициализации."""
        # Привести к типу `datetime` строковые значения
        # полей с датами.  Указания типа поля `datetime`
        # в dataclass'е не достаточно.
        for own_field in fields(type(self)):
            if own_field.type == datetime:
                value = getattr(self, own_field.name)
                if isinstance(value, str):
                    setattr(self, own_field.name, parse(value))


@dataclass
class Genre(SQLiteData):
    """Объектное представление строк таблицы genre."""

    name: str
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class FilmWork(SQLiteData):
    """Объектное представление строк таблицы film_work."""

    title: str
    description: str
    type: str
    creation_date: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    file_path: str = ''
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person(SQLiteData):
    """Объектное предславление строк таблицы person."""

    full_name: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmWork(SQLiteData):
    """Объектное предславление строк таблицы genre_film_work."""

    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created_at: datetime = field(default_factory=datetime.now)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmWork(SQLiteData):
    """Объектное предславление строк таблицы person_film_work."""

    role: str
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    created_at: datetime = field(default_factory=datetime.now)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


SOURCE_MAPPING = {
    FilmWork: 'film_work',
    Person: 'person',
    Genre: 'genre',
    GenreFilmWork: 'genre_film_work',
    PersonFilmWork: 'person_film_work',
}


DESTINATION_MAPPING = {
    Person: {
        'destination_table': 'person',
        'attribute_to_column': {
             'id': 'id',
             'full_name': 'full_name',
             'created_at': 'created',
             'updated_at': 'modified',
        },
    },
    FilmWork: {
        'destination_table': 'film_work',
        'attribute_to_column': {
            # Имя атрибута и соответствующий ему столбец в базе.
            'id': 'id',
            'title': 'title',
            'description': 'description',
            'rating': 'rating',
            'type': 'type',
            'creation_date': 'creation_date',
            'created_at': 'created',
            'updated_at': 'modified',
        },
    },
    Genre: {
        'destination_table': 'genre',
        'attribute_to_column': {
             'id': 'id',
             'name': 'name',
             'description': 'description',
             'created_at': 'created',
             'updated_at': 'modified',
        },
    },
    GenreFilmWork: {
        'destination_table': 'genre_film_work',
        'attribute_to_column': {
             'id': 'id',
             'genre_id': 'genre_id',
             'film_work_id': 'film_work_id',
             'created_at': 'created',
        },
    },
    PersonFilmWork: {
        'destination_table': 'person_film_work',
        'attribute_to_column': {
             'id': 'id',
             'person_id': 'person_id',
             'role': 'role',
             'film_work_id': 'film_work_id',
             'created_at': 'created',
        },
    },
}
