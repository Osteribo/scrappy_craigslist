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
    # this is the final url with corrected formating using quote_plus
    # which will fill in any spaces in the search term string
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # Getting the Webpage, creating a Response object.
    response = requests.get(final_url)
    # Extracting the source code of the page.
    data = response.text
    # Passing the source code to Beautiful Soup to create a
    # BeautifulSoup object for it.
    soup = BeautifulSoup(data, features="html.parser")
    # Extracting all the <a> tags whose class name is
    #  'results-title' into a list. 
    post_listings = soup.find_all('li', {'class': 'result-row'})
    # post_title = post_listings[0].find(class_='result-title').text

    # post_url = post_listings[0].find('a').get('href')
    # post_price = post_listings[0].find(class_='result-price').text
    
    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        final_postings.append((post_title, post_url, post_price))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
