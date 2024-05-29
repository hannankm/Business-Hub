# search/views.py
from django.shortcuts import render
import requests
from django.conf import settings

def wikipedia_search(query):
    url = settings.WIKIPEDIA_API_URL
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    return response.json()

def search_view(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        response = wikipedia_search(query)
        results = response.get('query', {}).get('search', [])
    return render(request, 'search/results.html', {'query': query, 'results': results})
