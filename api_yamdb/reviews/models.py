from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_year

CHOICES = tuple((x, str(x)) for x in range(1, 11))


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE_CHOICES = (
        (USER, 'user'),
        (ADMIN, 'administrator'),
        (MODERATOR, 'moderator')
    )

    confirmation_code = models.TextField(
        'код подтверждения',
        blank=True,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Уровень пользователя',
        choices=ROLE_CHOICES,
        max_length=40,
        blank=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-username',)


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(
        'Название категории',
        max_length=250
    )
    slug = models.SlugField(
        'Слаг категории',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-slug',)

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(
        'Название жанра',
        max_length=250
    )
    slug = models.SlugField(
        'Слаг жанра',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-slug',)

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        'Название',
        max_length=200,
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    year = models.PositiveSmallIntegerField(
        'Год',
        validators=(validate_year,),
        db_index=True
    )
    description = models.TextField(
        'Описание',
        max_length=256,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва',
        max_length=500
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now=True, db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.IntegerField(choices=CHOICES)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='the_only_one_review'
            ),
        )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.CharField(
        verbose_name='Комментарий к отзыву',
        help_text='Введите текст',
        max_length=100
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='АВтор комментария',
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now=True, db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
