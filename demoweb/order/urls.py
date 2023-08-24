from django.urls import path

from . import views

app_name = "order"
urlpatterns = [
    path('total/',views.total, name="total"),
    path('percent/',views.percent, name="percent"),
   
    
]
