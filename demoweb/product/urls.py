from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "product"
urlpatterns = [
     path('',views.index, name="index"),
     path('<int:id>/',views.detail, name="detail"),
     path('information/<int:id>/',views.infor, name="infor"),
     path('cart/',views.cart,name='cart'),
     path('register1/',views.register,name='register'),
     path( 'login/',auth_views.LoginView.as_view(template_name="product/login.html"), name="login"),
     path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
]    
