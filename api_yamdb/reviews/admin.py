from django.contrib import admin

from .models import Category, Genre, Title, User
from .models import Review, Comment
from api_yamdb.settings import EMPTY_VALUE_DISPLAY


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
        'description',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'role',
        'bio'
    )
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title'
    )
    search_fields = ('author',)
    list_filter = ('author',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'review'
    )
    search_fields = ('author',)
    list_filter = ('author',)
    empty_value_display = EMPTY_VALUE_DISPLAY
