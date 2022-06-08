import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TimeStampedMixin(models.Model):
    """Модель с метками времени создания и редактирования."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Модель с UUID в качестве основного ключа."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Жанр фильма."""

    name = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True)

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class FilmWork(UUIDMixin, TimeStampedMixin):
    """Фильмы и телешоу."""

    MIN_RATING = 0
    MAX_RATING = 100

    class Type(models.TextChoices):
        MOVIE = 'MV', 'Movie'
        TV_SHOW = 'TV', 'TV Show'

    title = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True)
    creation_date = models.DateField()
    rating = models.FloatField(
        'rating',
        blank=True,
        validators=[
            MinValueValidator(MIN_RATING),
            MaxValueValidator(MAX_RATING),
        ],
    )
    type = models.CharField('type', max_length=2, choices=Type.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = 'фильм'
        verbose_name_plural = 'фильмы'

    def __str__(self):
        return self.title

   
class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"genre_film_work'



class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('full name', max_length=255)
    roles = models.ManyToManyField(FilmWork, through='PersonFilmWork')

    class Meta:
        db_table = 'content\".\"person'
        verbose_name = 'персона'
        verbose_name_plural = 'персоны'

    def __str__(self):
        return self.full_name


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField('name', max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"person_film_work'
