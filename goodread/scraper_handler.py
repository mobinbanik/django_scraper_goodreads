import requests
from bs4 import BeautifulSoup

from django.conf import settings
from .models import (
    SearchGroupByKeywordItem,
    SearchBookByKeywordItem,
    SearchByKeyword,
    Book,
    Author,
    Genre,
    Group, BookGenre
)


class ScraperHandler:
    def __init__(self, base_url, search_url):
        self.base_url = base_url
        self.search_url = search_url

    @staticmethod
    def request_to_target_url(url):
        """Send request to target url.

        :param url: url to scrape
        :return:
        """
        # print('URL:', url)
        return requests.get(url, verify=True)

    def search_by_keyword(self, search_by_keyword_instance: SearchByKeyword) \
            -> list[SearchGroupByKeywordItem | SearchBookByKeywordItem]:
        """Search by keyword in target url.

        :param search_by_keyword_instance: SearchByKeyword instance
        :return: list of SearchGroupByKeywordItem or SearchBookByKeywordItem instances
        """
        search_items = list()

        # Navigate in pages
        for page in range(1, search_by_keyword_instance.page_count + 1):
            # Send request
            response = self.request_to_target_url(
                self.search_url.format(
                    query=search_by_keyword_instance.keyword,
                    page=page,
                    search_type=search_by_keyword_instance.search_type,
                    tab=search_by_keyword_instance.search_type,
                )
            )

            if response.status_code == 200:
                # Parse scraped data
                soup = BeautifulSoup(response.text, 'html.parser')
                search_items += self.extract_search_items(
                    search_by_keyword=search_by_keyword_instance,
                    soup=soup,
                )

        if search_by_keyword_instance.search_type == 'books':
            for search_item in search_items:
                book, genres = self.parse_book_detail(url=search_item.url)
                data = {
                    'title': book.title,
                    'author': book.author.full_name,
                    'description': book.description,
                    'thumbnail': book.thumbnail,
                    'genres': genres,
                }
                # Todo
                print(data)
        elif search_by_keyword_instance.search_type == 'groups':
            for search_item in search_items:
                group = self.parse_group_detail(url=search_item.url)
                data = {
                    'title': group.title,
                    'thumbnail': group.thumbnail,
                }
                # TODO
                print(data)

        # Return items
        return search_items

    def extract_search_items(self, search_by_keyword: SearchByKeyword, soup: BeautifulSoup):
        """Find target html tag and extract data from the element.

        :param search_by_keyword: SearchByKeyword instance
        :param soup: BeautifulSoup instance
        :return: list of SearchGroupByKeyword or SearchBookByKeywordItem instances
        """
        search_items = list()

        # Find a tags
        search_result_items = soup.find_all(
            'a',
            attrs={'class': settings.GOOD_READS_ITEM_CLASS[search_by_keyword.search_type]},
        )

        # Clean the <a> tags and append to list
        for a in search_result_items:
            search_items.append(self.parse_search_item(search_by_keyword, a))

        return search_items

    def parse_search_item(self, search_by_keyword: SearchByKeyword, a_tag):
        """Create proper instance from search results.

        :param search_by_keyword: SearchByKeyword instance
        :param a_tag: PageElement in bs4
        :return: SearchGroupByKeywordItem or SearchBookByKeywordItem
        """
        if search_by_keyword.search_type == 'books':
            return SearchBookByKeywordItem.objects.create(
                search_by_keyword=search_by_keyword,
                title=a_tag.text.strip(),
                url=self.base_url + a_tag['href'],
            )
        if search_by_keyword.search_type == 'groups':
            return SearchGroupByKeywordItem.objects.create(
                search_by_keyword=search_by_keyword.keyword,
                title=a_tag.text.strip(),
                url=self.base_url + a_tag['href'],
            )

    def parse_book_detail(self, url):
        response = self.request_to_target_url(url=url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', attrs={'class': 'Text Text__title1'}).text
        description = soup.find(
            'div',
            attrs={
                'class': 'DetailsLayoutRightParagraph__widthConstrained',
            },
        ).find_next('span').text
        thumbnail = soup.find(
            'img',
            attrs={'class': 'ResponsiveImage', 'role': 'presentation'},
        )['src']
        author, _ = self.parse_author(soup=soup)
        book, _ = Book.objects.get_or_create(
            author=author,
            title=title,
            description=description,
            thumbnail=thumbnail,
            html_source_code=response.text,
        )
        genres = self.parse_genre(soup=soup)

        for genre in genres:
            BookGenre.objects.get_or_create(
                book=book,
                genre=genre,
            )
        return book, genres

    @staticmethod
    def parse_author(soup):
        full_name = soup.find('span', attrs={'class': 'ContributorLink__name'}).text
        return Author.objects.get_or_create(full_name=full_name)

    @staticmethod
    def parse_genre(soup):
        genres = list()
        genre_soup = soup.find('ul', attrs={'class': 'CollapsableList', 'aria-label': 'Top genres for this book'})
        for genre in genre_soup.findAll('span', attrs={'class': 'Button__labelItem'}):
            if genre.text != '...more':
                new_genre, _ = Genre.objects.get_or_create(title=genre.text)
                genres.append(new_genre)

        return genres

    def parse_group_detail(self, url):
        response = self.request_to_target_url(url=url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('div', attrs={'class': 'mainContentFloat'}).findNext('h1').text
        thumbnail = soup.find('a', attrs={'class': 'groupPicLink', }).find_next('img')['src']
        group_type = soup.find('div', string='group type')
        group_type = group_type.find_next_sibling('div')
        group, _ = Group.objects.get_or_create(
            title=title,
            thumbnail=thumbnail,
            html_source_code=response.text,
            group_type=group_type.text,
        )

        return group
