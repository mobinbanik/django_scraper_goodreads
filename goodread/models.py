from abc import abstractmethod
from django.db import models
from django.conf import settings


# Create your models here.
class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Updated At')

    class Meta(object):
        # This makes this class no longer applied in migration
        abstract = True

    @abstractmethod
    def __str__(self):
        raise NotImplementedError('Implement __str__ method')


class Author(BaseModel):
    full_name = models.CharField(
        max_length=128,
        verbose_name='Full Name',
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.full_name


class Genre(BaseModel):
    title = models.CharField(
        max_length=128,
        verbose_name='Genre Title',
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.title


class Book(BaseModel):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Author',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Title',
        null=False,
        blank=False,
    )
    description = models.TextField(
        verbose_name='Description',
        null=False,
        blank=False,
    )
    thumbnail = models.TextField()
    html_source_code = models.TextField(
        verbose_name='Html source code',
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class BookGenre(BaseModel):
    book = models.ForeignKey(
        Book,
        models.CASCADE,
        related_name='book_genres',
    )
    genre = models.ForeignKey(
        Genre,
        models.CASCADE,
        related_name='book_genres',
    )

    def __str__(self):
        return f'{self.book.title} ({self.genre.title})'

    class Meta:
        verbose_name = 'Book Genre'
        verbose_name_plural = 'Book Genres'


class Group(BaseModel):
    title = models.CharField(
        max_length=255,
        verbose_name='Title',
        null=False,
        blank=False,
    )
    group_type = models.CharField(
        max_length=255,
        verbose_name='Group Type',
        null=True,
        blank=True,
    )
    thumbnail = models.TextField()
    html_source_code = models.TextField(
        verbose_name='HTML Source Code',
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Keyword(BaseModel):
    title = models.CharField(
        max_length=255,
        verbose_name='Title',
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'


class SearchByKeyword(BaseModel):
    keyword = models.ForeignKey(
        Keyword,
        models.CASCADE,
        related_name='searches',
    )
    search_type = models.CharField(
        max_length=64,
        verbose_name='Search Type',
        null=False,
        blank=False,
        default=settings.SEARCH_TYPE,
    )
    page_count = models.IntegerField(
        verbose_name='Page Count',
        null=False,
        blank=False,
        default=settings.SEARCH_PAGE_COUNT,
    )

    def __str__(self):
        return self.keyword.title

    class Meta:
        verbose_name = 'Search By Keyword'
        verbose_name_plural = 'Search By Keywords'


class SearchBookByKeywordItem(BaseModel):
    search_by_keyword = models.ForeignKey(
        SearchByKeyword,
        models.CASCADE,
        related_name='search_book_by_keyword_items',
        verbose_name='Search By Keyword',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Title',
        null=False,
        blank=False,
    )
    url = models.TextField(
        verbose_name='URL',
        null=False,
        blank=False,
    )
    book = models.ForeignKey(
        Book,
        models.CASCADE,
        related_name='search_book_by_keyword_items',
        verbose_name='Book',
    )
    is_scraped = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}({self.search_by_keyword.keyword.title})'

    class Meta:
        verbose_name = 'Book Search By Keyword Item'
        verbose_name_plural = 'Book Search By Keyword Items'


class SearchGroupByKeywordItem(BaseModel):
    search_by_keyword = models.ForeignKey(
        SearchByKeyword,
        models.CASCADE,
        related_name='search_group_by_keyword_items',
        verbose_name='Search By Keyword',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Title',
        null=False,
        blank=False,
    )
    url = models.TextField(
        verbose_name='URL',
        null=False,
        blank=False,
    )

    group = models.ForeignKey(
        Group,
        models.CASCADE,
        verbose_name='Group',
        related_name='search_group_by_keyword_items',
    )
    is_scraped = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}({self.search_by_keyword.keyword.title})'

    class Meta:
        verbose_name = 'Group Search By Keyword Item'
        verbose_name_plural = 'Group Search By Keyword Items'
