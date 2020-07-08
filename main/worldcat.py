import requests
import json
from io import BytesIO
from lxml import etree
from django.conf import settings
from bs4 import BeautifulSoup

api_key = settings.WORLDCAT_API

def search_worldcat(query:str):
    url = f"http://www.worldcat.org/webservices/catalog/search/worldcat/opensearch?q={query}&wskey={api_key}"
    response = requests.get(url)
    tree = etree.parse(BytesIO(response.content))
    #print(etree.tostring(tree, encoding='utf8', method='xml'))

    data = []
    for element in tree.findall("{http://www.w3.org/2005/Atom}entry"):
        row= {}
        for this in element.iter():
            if this.tag.endswith("author"):
                row['author'] =''.join(this.itertext()).replace('\n            ','').replace('\n        ','').replace(', author.','')
            if this.tag.endswith("title"):
                row['title'] =''.join(this.itertext())
            if this.tag.endswith("id"):
                row['id'] =''.join(this.itertext())
            if this.tag.endswith("summary"):
                row['summary'] =''.join(this.itertext())
        data.append(row)
    return data

def worldcat_soup(url:str):
    result = {}
    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    result['thumbnail'] = soup.findAll("img", {"class": "cover"})[0]['src']
    result['title'] = soup.findAll("h1", {"class": "title"})[0].text
    authors = soup.findAll("td", {"id": "bib-author-cell"})
    authors = authors[0].findChildren("a" , recursive=False)
    result['authors'] = [author.text for author in authors]
    subjects = soup.findAll("li", {"class": "subject-term"})
    data = [] 
    for subject in subjects:
        subject = subject.findChildren("a" , recursive=False)
        subject = subject[0].text
        data.append(subject)
    result['subjects'] = data
    return result