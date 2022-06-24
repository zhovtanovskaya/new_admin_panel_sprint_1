import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


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

    name = models.CharField(_('name'), unique=True, max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class FilmWork(UUIDMixin, TimeStampedMixin):
    """Фильм или телешоу."""

    MIN_RATING = 0
    MAX_RATING = 100

    class Type(models.TextChoices):
        MOVIE = 'MV', _('Movie')
        TV_SHOW = 'TV', _('TV Show')

    type = models.CharField(_('type'), max_length=2, choices=Type.choices)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(MIN_RATING),
            MaxValueValidator(MAX_RATING),
        ],
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')

    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = _('film work')
        verbose_name_plural = _('film works')

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    """Связь "много-ко-многим" между фильмами и жанрами."""

    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre, verbose_name=_('genre'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('film_work', 'genre')
        db_table = 'content\".\"genre_film_work'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.genre.name


class Person(UUIDMixin, TimeStampedMixin):
    """Участник команды производства фильма."""

    full_name = models.CharField(_('full name'), max_length=255)
    roles = models.ManyToManyField(FilmWork, through='PersonFilmWork')

    class Meta:
        db_table = 'content\".\"person'
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


class PersonFilmWork(UUIDMixin):
    """Связь "много-ко-многим" между фильмами и участниками."""

    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    person = models.ForeignKey(
        Person, verbose_name=_('person'), on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('film_work', 'person', 'role')
        db_table = 'content\".\"person_film_work'
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __str__(self):
        return self.role
