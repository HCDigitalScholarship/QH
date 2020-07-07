from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from main.utils import parse_results, search, format_query
from django.http import JsonResponse, HttpResponse
from main.models import Item, Author, Category
from django.utils.dateparse import parse_date

# Create your views here.
def home(request):
    context = {}
    return render(request, 'index.html', context)

def collection(request):
    context = {}
    context['items'] = Item.objects.all()
    return render(request, 'collection.html', context)

@staff_member_required
def edit(request):
    context = {}
    if request.POST: 
        query = request.POST
        query = format_query(**query)
        response = search(query)
        results = parse_results(response)
        context['results'] = results
    
    return render(request, 'edit.html', context)

@staff_member_required
def add_book(request):
    if request.POST: 
        data = request.POST.get("data", None)
        data = eval(data)
        
        book, created = Item.objects.update_or_create(
            title = data['title'],
            raw_json = str(data),
        )
        book.published_date = parse_date(data['publishedDate'])
        book.identifier = data['industryIdentifiers'][0]['identifier']
        book.language = data['language']
        book.publisher = data['publisher']
        book.page_count= data['pageCount']
        book.thumbnail = data['imageLinks']['thumbnail']
        book.print_type = data['printType']
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
