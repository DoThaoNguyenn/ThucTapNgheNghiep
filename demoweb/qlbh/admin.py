from django.contrib import admin
from .models import categories, products, orders, order_detail, payments
# Register your models here.

admin.site.register(categories)
admin.site.register(products)
admin.site.register(payments)
admin.site.register(orders)
admin.site.register(order_detail)
