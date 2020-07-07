from django.contrib import admin
from main.models import Book
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


admin.site.register(Book, BookAdmin)