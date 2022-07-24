from itertools import product
from unicodedata import category
from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}

@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','category','price',"available"]
    prepopulated_fields = {"slug":("name",)}

admin.site.register(Customer )
admin.site.register(Order )
admin.site.register(Blogs)
admin.site.register(editOrders)
admin.site.register(signupasseller)
admin.site.register(adminaccount)
admin.site.register(contactform)
