from django import forms
from django.forms import ModelForm
from .models import Product

class Product_create_form(ModelForm):
    class Meta:
        model= Product
        fields='__all__'
    #     # exclude = ['cost', 'quantity', 'discount', 'image']


# class Product_create_form(forms.Form):
#     category= forms.CharField()
#     title =  forms.CharField()
#     cost = forms.IntegerField()
#     quantity = forms.IntegerField()
#     discount = forms.IntegerField()
#     image = forms.ImageField()