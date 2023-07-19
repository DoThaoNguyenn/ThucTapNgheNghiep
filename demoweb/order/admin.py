from django.contrib import admin
from .models import Users, Order, Order_detail
# from .form import UsersCreationFrom
from django.contrib.auth.admin import UserAdmin
# Register your models here.

# class UsersAdmin(UserAdmin):
#     model = users
#     add_form = UsersCreationFrom
#     list_display = ('email', 'name')
#     ordering = ('email','name')
#     search_fields = ('email','name','phone')

#     fieldsets = (
#         ('User profile', {'fields': ('email', 'password', 'name', 'address', 'phone')}),
      
#     )
#     add_fieldsets = (
#         (None, {
#             'fields': ('email', 'password1', 'password2')}
#         ),
#     )

admin.site.register(Users, UserAdmin)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','quantity','total']
@admin.register(Order_detail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity']

