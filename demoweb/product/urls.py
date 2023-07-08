from django.urls import path

from . import views

app_name = "product"
urlpatterns = [
     path('',views.index, name="index"),
     path('<int:id>/',views.detail, name="detail"),
     path('information/<int:id>/',views.infor, name="infor"),
]
