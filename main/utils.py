import requests
from django.conf import settings
api_key = settings.GOOGLE_API

def format_query(**kwargs):
    query = ""
    if 'q' in kwargs:
        query += kwargs['q']    
    if 'title' in kwargs:
        query += '+intitle:' + kwargs['title']
    if 'author' in kwargs: 
        query += '+inauthor:' + kwargs['author']
    if 'publisher' in kwargs: 
        query += '+inpublisher:' + kwargs['publisher']
    if 'subject' in kwargs: 
        query += '+subject:' + kwargs['subject']
    if 'isbn' in kwargs: 
        query += '+isbn:' + kwargs['isbn']
    if 'lccn' in kwargs: 
        query += '+lccn:' + kwargs['lccn']
    if 'oclc' in kwargs: 
        query += '+oclc:' + kwargs['oclc']
    return query 

def search(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}" 
    response = requests.get(url)
    return response.json()

def parse_results(response):
    results = []
    for book in response['items']:
        results.append(book['volumeInfo'])
    return results 