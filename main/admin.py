from django.contrib import admin
from main.models import Item, Author, Category
# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


admin.site.register(Item, ItemAdmin)

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


admin.site.register(Category, CategoryAdmin)

class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


admin.site.register(Author, AuthorAdmin)