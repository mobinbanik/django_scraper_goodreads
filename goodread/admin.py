from django.contrib import admin
from django.contrib.admin import register

from .models import (
    Author, Genre, Book, BookGenre,
    Group, Keyword, SearchByKeyword,
    SearchBookByKeywordItem, SearchGroupByKeywordItem,
)


# Register your models here.
class BaseAdminModel(admin.ModelAdmin):
    actions = ('make_activate', 'make_deactivate')

    @admin.action
    def make_deactivate(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action
    def make_activate(self, request, queryset):
        queryset.update(is_active=True)


@register(Author)
class AuthorAdmin(BaseAdminModel):
    list_display = (
        'id',
        'full_name',
        'is_active',
        'created_at',
        'updated_at',
    )
    list_display_links = ('id', 'full_name')
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)


@register(Genre)
class GenreAdmin(BaseAdminModel):
    list_display = (
        'id',
        'title',
        'is_active',
        'created_at',
        'updated_at',
    )
    list_display_links = ('id', 'title')
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)


@register(Book)
class BookAdmin(BaseAdminModel):
    list_display = (
        'id',
        'title',
        'author',
        'description',
        'is_active',
        'created_at',
        'updated_at',
    )
    list_display_links = ('id', 'title')
    list_filter = ('is_active', 'created_at', 'updated_at', 'author')
    list_editable = ('is_active',)


@register(BookGenre)
class BookGenreAdmin(BaseAdminModel):
    list_display = (
        'id',
        'book',
        'genre',
        'is_active',
        'created_at',
        'updated_at',
    )
    list_display_links = ('id', 'book')
    list_filter = ('is_active', 'created_at', 'updated_at', 'book', 'genre')
    list_editable = ('is_active',)


@register(Group)
class GroupAdmin(BaseAdminModel):
    list_display = ('id', 'title', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)


@register(Keyword)
class KeywordAdmin(BaseAdminModel):
    list_display = ('id', 'title', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    list_filter = ('is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)


@register(SearchByKeyword)
class SearchByKeywordAdmin(BaseAdminModel):
    list_display = ('id', 'keyword', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'keyword')
    list_filter = ('is_active', 'created_at', 'updated_at', 'keyword')
    list_editable = ('is_active',)


@register(SearchBookByKeywordItem)
class SearchBookByKeywordItemAdmin(BaseAdminModel):
    list_display = (
        'id',
        'search_by_keyword',
        'book',
        'is_scraped',
        'title',
        'url',
        'is_active',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'search_by_keyword')
    list_filter = (
        'is_active',
        'is_scraped',
        'created_at',
        'updated_at',
        'search_by_keyword',
        'book',
    )
    list_editable = ('is_active',)


@register(SearchGroupByKeywordItem)
class SearchGroupByKeywordItemAdmin(BaseAdminModel):
    list_display = (
        'id',
        'search_by_keyword',
        'group',
        'is_scraped',
        'title',
        'url',
        'is_active',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'search_by_keyword')
    list_filter = (
        'is_active',
        'is_scraped',
        'created_at',
        'updated_at',
        'search_by_keyword',
        'group',
    )
    list_editable = ('is_active',)
