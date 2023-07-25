from django import forms
from django.forms import ModelForm
from .models import Product, Category, Product_information
import re
from django.core.exceptions import ObjectDoesNotExist
from order.models import Users, Order, Order_detail


class Product_create_form(ModelForm):
    class Meta:
        model= Product
        fields=['category', 'title', 'cost', 'quantity', 'discount', 'image']
        
    #     # exclude = ['cost', 'quantity', 'discount', 'image']

class Category_create_form(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class Add_Product_information(ModelForm):
    class Meta:
        model = Product_information
        fields = '__all__'

class Register_form(forms.Form):
    # class Meta:
    #     model = Users
    #     fields = ['username','email','password1','password2']
    #     widgets ={
    #         'username':forms.CharField(label='Tài khoản'),
    #         'email': forms.EmailField(label='Email'),
    #         'password1': forms.PasswordInput(attrs={'label': 'Nhập mật khẩu'}),
    #         'password2': forms.PasswordInput(attrs={'label': 'Nhập lại mật khẩu'}),
    #     }
    
    username= forms.CharField(label='Tài khoản', max_length=30)
    email=forms.EmailField(label='Email')
    password1=forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2=forms.CharField(label='Nhâp lại mật khẩu',widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1=self.cleaned_data['password1']
            password2=self.cleaned_data['password2']
            if password1==password2 and password1: 
                return password2
        raise forms.ValidationError('Mật khẩu không hợp lệ')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$',username):
            raise forms.ValidationError("Tên tài khoản không hợp lệ")
        try:
            Users.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Tài khoản đã tồn tại')

    def save(self):

        Users.objects.create_user(username=self.cleaned_data['username'],email=self.cleaned_data['email'],password=self.cleaned_data['password1'])
            


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order 
        fields = ['menthod','note']
        labels = {'menthod':'Phương thức thanh toán:', 'note':'Ghi chú:'}

    widgets = {
            'menthod': forms.Select(attrs={'class':'form-control'}),
            'note': forms.Textarea(attrs={'class':'form-control'}),
    }

class UserInformationForm(forms.ModelForm):
    class Meta:
        model = Users
        fields =['first_name', 'last_name','phone','address']
        labels ={'first_name':'Họ:', 'last_name':'Tên:','phone':'Số điện thoại:', 'address':'Địa chỉ:'}
       
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
        }