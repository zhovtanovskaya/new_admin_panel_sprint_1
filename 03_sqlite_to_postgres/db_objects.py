"""Python-представление объектов, импортируемых из SQLite."""

import uuid
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