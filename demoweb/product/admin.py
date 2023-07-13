from django.contrib import admin
from .models import Category, Product, Product_information
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Product_information)
