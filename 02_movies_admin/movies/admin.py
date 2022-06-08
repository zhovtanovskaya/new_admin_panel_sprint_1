from django.contrib import admin

from .models import FilmWork, Genre, GenreFilmWork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmWork


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
