from django.urls import path

from . import views

app_name = "product"
urlpatterns = [
     path('',views.index, name="index"),
     path('add_to_cart/<int:id>/',views.add_to_cart, name="add_to_cart"),
     path('<int:id>/',views.detail, name="detail"),
     path('information/<int:id>/',views.infor, name="infor"),
     path('cart/',views.show_cart, name="show_cart"),
     path('create_product/',views.create_product,name='create_product'),
     
]
