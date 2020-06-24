import requests
# quote_plus auto add "+" to strings
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

# Create your views here.

BASE_CRAIGSLIST_URL = "https://seattle.craigslist.org/search/?query={}"


def home(request):
    return render(request, 'base.html')


def new_search(request):
    # get inputed search text
    search = request.POST.get('search')
    # add search to database for tracking
    models.Search.objects.create(search=search)
    # this is the final url with corrected formating using quote_plus which will fill in any spaces in the search term string
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # Getting the Webpage, creating a Response object.
    response = requests.get(final_url)
    # Extracting the source code of the page.
    data = response.text
    # Passing the source code to Beautiful Soup to create a BeautifulSoup object for it.
    soup = BeautifulSoup(data, features="html.parser")
    # Extracting all the <a> tags whose class name is 'results-title' into a list. 
    post_titles = soup.find_all('a', {'class': 'result-title'})

    print(post_titles[0])

    stuff_for_frontend = {
        'search': search,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
