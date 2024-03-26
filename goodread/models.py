from abc import abstractmethod
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    Updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Updated At')

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
    )

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.full_name


class Genre(BaseModel):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return self.title


class Book(BaseModel):
    def __init__(self, author: Author, title: str, description: str, thumbnail, html_source_code):
        self.author = author
        self.title = title
        self.description = description
        self.thumbnail = thumbnail
        self.html_source_code = html_source_code

    def __str__(self):
        return self.title


class BookGenre(BaseModel):
    def __init__(self, book, genre):
        self.book = book
        self.genre = genre

    def __str__(self):
        return self.book + " " + self.genre


class Group(BaseModel):
    def __init__(self, title: str, group_type: str, thumbnail, html_source_code):
        self.title = title
        self.group_type = group_type
        self.thumbnail = thumbnail
        self.html_source_code = html_source_code

    def __str__(self):
        return self.title


class Keyword(BaseModel):
    def __init__(self, title: str):
        self.title = title

    def __str__(self):
        return self.title


class SearchByKeyword(BaseModel):
    def __init__(self, title, keyword: Keyword, search_type, page_count=SEARCH_PAGE_COUNT):
        self.title = title
        self.keyword = keyword
        self.search_type = search_type
        self.page_count = page_count
        self.created_at = datetime.now()

    def __str__(self):
        return self.title


class SearchBookByKeywordItem(BaseModel):
    def __init__(self, search_by_keyword: SearchByKeyword, title, url):
        self.search_by_keyword = search_by_keyword
        self.title = title
        self.url = url
        self.book = None

    def __str__(self):
        return f'{self.title}({self.search_by_keyword.keyword.title})'


class SearchGroupByKeywordItem(BaseModel):
    def __init__(self, search_by_keyword: SearchByKeyword, title, url):
        self.search_by_keyword = search_by_keyword
        self.title = title
        self.url = url
        self.group = None

    def __str__(self):
        return f'{self.title}({self.search_by_keyword.keyword.title})'
