from django.shortcuts import render
from django.conf import settings

from .forms import SearchByKeywordForm
from .models import SearchByKeyword, Keyword
from .scraper_handler import ScraperHandler


# Create your views here.
def search_by_keyword_view(request):
    if request.method == 'POST':
        form = SearchByKeywordForm(request.POST)
        if form.is_valid():
            data = {
                'keyword': form.cleaned_data['keyword'],
                'search_type': form.cleaned_data['search_type'],
                'page_count': form.cleaned_data['page_count'],
            }

            keyword, _ = Keyword.objects.get_or_create(
                title=form.cleaned_data['keyword'],
            )
            search_by_keyword_instance = SearchByKeyword.objects.create(
                keyword=keyword,
                search_type=form.cleaned_data['search_type'],
                page_count=form.cleaned_data['page_count']
            )

            scraper_handler = ScraperHandler(
                base_url=settings.GOOD_READS_BASE_URL,
                search_url=settings.GOOD_READS_SEARCH_URL,
            )

            search_results = scraper_handler.search_by_keyword(search_by_keyword_instance)

            return render(request, 'goodread/search.html', {'form': form})

    else:
        form = SearchByKeywordForm()

    return render(request, 'goodread/search.html', {'form': form})
