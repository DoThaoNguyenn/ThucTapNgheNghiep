from django.contrib import admin
from .models import Category, Product, Review

# Register your models here.

admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "cost", "quantity", "discount"]


# @admin.register(Product_information)
# class ProductAdmin(admin.ModelAdmin):
#     list_display =['product','author','pages','publisher']

admin.site.register(Review)
