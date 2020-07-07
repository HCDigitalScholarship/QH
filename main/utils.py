import requests
from django.conf import settings
import json 
api_key = settings.GOOGLE_API

def format_query(**kwargs):
    query = ""
    if 'q' in kwargs:
        query += kwargs['q']    
    else:
        query += '.'
    if 'title' in kwargs:
        if len(kwargs['title'][0]) > 0:
            query += '+intitle:' + kwargs['title'][0]
    if 'author' in kwargs: 
        if len(kwargs['author'][0]) > 0:
            query += '+inauthor:' + kwargs['author'][0]
    if 'publisher' in kwargs:
        if len(kwargs['publisher'][0]) > 0: 
            query += '+inpublisher:' + kwargs['publisher'][0]
    if 'subject' in kwargs: 
        if len(kwargs['subject'][0]) > 0:
            query += '+subject:' + kwargs['subject'][0]
    if 'isbn' in kwargs: 
        if len(kwargs['isbn'][0]) > 0:
            query += '+isbn:' + kwargs['isbn'][0]
    if 'lccn' in kwargs: 
        if len(kwargs['lccn'][0]) > 0:
            query += '+lccn:' + kwargs['lccn'][0]
    if 'oclc' in kwargs: 
        if len(kwargs['oclc'][0]) > 0:
            query += '+oclc:' + kwargs['oclc'][0]
    return query 

def search(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}" 
    response = requests.get(url)
    return response.json()

def parse_results(response):
    results = []
    try:
        for book in response['items']:
            results.append(book['volumeInfo'])
    except KeyError: # no response items
        pass
    return results 