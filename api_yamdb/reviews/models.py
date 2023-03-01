from django.db import models


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название роизведения',
        max_length=256,
    )
    year = models.IntegerField()
    description = models.TextField('Описание произведения')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True, null=True
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    title = models.ForeignKey(
        Title,
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.genre} <-> {self.title}'
