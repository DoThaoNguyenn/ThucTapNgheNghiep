from django.urls import path

from . import views

app_name = "qlbh"
urlpatterns = [
     path('',views.index, name="index"),
]
