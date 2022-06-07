import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class FilmWork(models.Model):
    MIN_RATING = 0
    MAX_RATING = 10

    class Type(models.TextChoices):
        MOVIE = 'MV', 'Movie'
        TV_SHOW = 'TV', 'TV Show'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True)
    creation_date = models.DateField()
    rating = models.FloatField(
        validators=[MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)])
    type = models.CharField('type', max_length=2, choices=Type.choices)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'фильм'
        verbose_name_plural = 'фильмы'

    def __str__(self):
        return self.title
