from django.contrib import admin
from .models import catogories, products, orders, order_detail, payments
# Register your models here.

admin.site.register(catogories)
admin.site.register(products)
admin.site.register(payments)
admin.site.register(orders)
admin.site.register(order_detail)
