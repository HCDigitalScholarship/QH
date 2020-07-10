from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from main.utils import parse_results, search, format_query
from django.http import JsonResponse, HttpResponse
from main.models import Item, Author, Category
from django.utils.dateparse import parse_date
from main.worldcat import search_worldcat, worldcat_soup
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    context = {}
    return render(request, 'index.html', context)

def collection(request):
    context = {}
    items = Item.objects.all()
    paginator = Paginator(items, 25) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['items'] = page_obj
    return render(request, 'collection.html', context)

@staff_member_required
def edit_book(request):
    context = {}
    if request.POST: 
        query = request.POST
        query = format_query(**query)
        response = search(query)
        results = parse_results(response)
        context['results'] = results
    
    return render(request, 'edit_book.html', context)

@staff_member_required
def edit_item(request):
    context = {}
    if request.POST: 
        query = request.POST.get('query',None)
        context['results'] = search_worldcat(query)
    return render(request, 'edit_item.html', context)

@staff_member_required
def add_item(request):
    if request.POST: 
        data = request.POST.get("data", None)
        data = worldcat_soup(data)
        book, created = Item.objects.update_or_create(
            title = data['title'],
            thumbnail= data['thumbnail'],
        )
        for author in data['authors']:
            author, created = Author.objects.get_or_create(name=author)
            book.authors.add(author.pk)
        for category in data['subjects']:
            category, created = Category.objects.get_or_create(name=category)
            book.categories.add(category.pk)
        book.save()
        
        return JsonResponse({"message": "Added " + book.title  })
    else:
        return HttpResponse("🧙 You are lost my friend.  Let the back button be your guide. 🧙")


@staff_member_required
def add_book(request):
    """An endpoint to handle ajax requests from edit.html. When a search result is clicked, its data is send here
    and added to the database"""
    if request.POST: 
        data = request.POST.get("data", None)
        data = eval(data)
        
        book, created = Item.objects.update_or_create(
            title = data['title'],
            raw_json = str(data),
        )
        book.published_date = parse_date(data['publishedDate'])
        book.identifier = data['industryIdentifiers'][0]['identifier']
        book.language = data.get('language',None)
        book.publisher = data.get('publisher', None)
        book.page_count= data.get('pageCount', None)
        book.thumbnail = data['imageLinks']['thumbnail']
        book.print_type = data.get('printType',None)
        for author in data['authors']:
            author, created = Author.objects.get_or_create(name=author)
            book.authors.add(author.pk)
        for category in data['categories']:
            category, created = Category.objects.get_or_create(name=category)
            book.categories.add(category.pk)
        book.save()
        if created:
            return JsonResponse({"message": "Added: " + book.title })
        else:
            return JsonResponse({"message": "Updated: " + book.title})
    else:
        return HttpResponse("🧙 You are lost my friend.  Let the back button be your guide. 🧙")
