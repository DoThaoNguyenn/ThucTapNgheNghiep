from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "product"
urlpatterns = [
     path('',views.index, name="index"),
     path('<int:id>/',views.detail, name="detail"),
     path('information/<int:id>/',views.infor, name="infor"),
     

     path('create_product/',views.create_product,name='create_product'),
     path('list_product/',views.list_product,name='list_product'),
     path('update_product/<int:id>/',views.update_product,name='update_product'),
     path('delete_product/<int:id>/',views.delete_product,name='delete_product'),
     path('add_product_information/<int:id>/',views.add_product_information,name='add_product_information'),

     path('list_category/',views.list_category,name='list_category'),
     path('create_category/',views.create_category,name='create_category'),
     path('update_category/<int:id>/',views.update_category,name='update_category'),
     path('delete_category/<int:id>/',views.delete_category,name='delete_category'),

     path('register/',views.register,name='register'),
     path( 'login/',auth_views.LoginView.as_view(template_name="product/login.html"), name="login"),
     path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),

     path('add_to_cart/<int:id>/',views.add_to_cart, name="add_to_cart"),
     path('remove_orderDetail/<int:id>/',views.remove_orderDetail, name="remove_orderDetail" ),
     path('minus_quantity/<int:id>/',views.minus_quantity, name="minus_quantity" ),
     path('plus_quantity/<int:id>/',views.plus_quantity, name="plus_quantity" ),
     path('show_cart/',views.show_cart, name="show_cart"),
     path('checkout/',views.checkout, name="checkout"),
     path('review_order/',views.review_order, name="review_order"),

]
