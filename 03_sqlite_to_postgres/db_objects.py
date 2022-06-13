"""Python-представление данных, импортируемых из SQLite."""

import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class FilmWork:
    """Объектное представление строк таблицы film_work."""

    title: str
    description: str
    type: str
    creation_date: str
    file_path: str = ''
    created_at: str = ''
    updated_at: str = ''
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Person:
    """Объектное предславление строк таблицы person."""

    full_name: str
    created_at: str = ''
    updated_at: str = ''
    id: uuid.UUID = field(default_factory=uuid.uuid4)
