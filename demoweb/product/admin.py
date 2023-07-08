from django.contrib import admin
from .models import category, product, product_information
# Register your models here.

admin.site.register(category)
admin.site.register(product)
admin.site.register(product_information)
