from django import forms
from .models import orders, payments




class status_form(forms.Form):
    status_field = forms.ChoiceField(choices = orders.status_choices, widget=forms.Select(), required=True)

class paymentmenthods_form(forms.Form):
    paymentmenthods_field = forms.ChoiceField(choices = payments.paymentmenthods_choices, widget=forms.Select(), required=True)   
    