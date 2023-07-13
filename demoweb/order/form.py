from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import order, users

class paymentmenthods_form(forms.Form):
    paymentmenthods_field = forms.ChoiceField(choices = order.paymentmenthods_choices, widget=forms.Select(), required=True)   


class UsersCreationFrom(UserCreationForm):
    class Meta:
        models = users
        fields = ['email', 'password', 'name', 'address', 'phone']