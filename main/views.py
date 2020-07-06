from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from main.utils import parse_results, search, format_query

# Create your views here.
def home(request):
    context = {}
    return render(request, 'index.html', context)

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