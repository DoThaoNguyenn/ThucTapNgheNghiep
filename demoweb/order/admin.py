from django.contrib import admin
from .models import Users, Order, Order_detail, Contact
# from .form import UsersCreationFrom
from django.contrib.auth.admin import UserAdmin

admin.site.register(Users, UserAdmin)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','quantity','total_price']
@admin.register(Order_detail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity']
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','number','email','message']

