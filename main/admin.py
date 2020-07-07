from django.contrib import admin
from main.models import Item
# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


admin.site.register(Item, ItemAdmin)