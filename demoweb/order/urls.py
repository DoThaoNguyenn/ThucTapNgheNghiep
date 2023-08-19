from django.urls import path

from . import views

app_name = "order"
urlpatterns = [
    path('total/',views.total, name="total"),
    path('percent/',views.percent, name="percent"),
    path('top5/',views.top5, name="top5"),
]
