from django import forms
from .models import order, payment




class status_form(forms.Form):
    status_field = forms.ChoiceField(choices = order.status_choices, widget=forms.Select(), required=True)

class paymentmenthods_form(forms.Form):
    paymentmenthods_field = forms.ChoiceField(choices = payment.paymentmenthods_choices, widget=forms.Select(), required=True)   