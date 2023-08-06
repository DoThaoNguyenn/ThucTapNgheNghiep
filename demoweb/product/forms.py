from django import forms
from django.forms import ModelForm
from .models import Product, Category, Review
import re
from django.core.exceptions import ObjectDoesNotExist
from order.models import Users, Order, Order_detail,Contact
from vi_address.models import City, District, Ward

class Product_create_form(ModelForm):
    class Meta:
        model= Product
        # fields=['category', 'title', 'cost', 'quantity', 'discount', 'image']
        fields = '__all__'
  

class Category_create_form(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

# class Add_Product_information(ModelForm):
#     class Meta:
#         model = Product_information
#         fields = '__all__'

class Register_form(forms.Form):
 
    
    username= forms.CharField(label='Tài khoản', max_length=30)
    email=forms.EmailField(label='Email')
    password1=forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={'class': 'myform','id':'password'}))
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
            



class UserInformationForm(forms.ModelForm):
    
    city =forms.ModelChoiceField(label = 'Tỉnh/Thành phố',queryset = City.objects.all(), widget=forms.Select(attrs={"class": "form-control","hx-get":"/load-districts/","hx-target":"#id_district"}))
    district =forms.ModelChoiceField(label = 'Quận/Huyện:',queryset = District.objects.none(), widget=forms.Select(attrs={"class": "form-control","hx-get":"/load-wards/","hx-target":"#id_ward"}))
    ward =forms.ModelChoiceField(label = 'Phường/Xã:',queryset = Ward.objects.none(), widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = Users
        fields =['first_name', 'last_name','phone','city','district','ward','street']
        labels ={'first_name':'Họ:', 'last_name':'Tên:','phone':'Số điện thoại:','street':'Tên đường'}
       
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'street': forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      

        if 'city' in self.data:
            city_id =self.data.get("city")
            self.fields['district'].queryset = District.objects.filter(parent_code=city_id)
        if 'district' in self.data:
            city_id =self.data.get("district")
            self.fields['ward'].queryset = Ward.objects.filter(parent_code=city_id)

        # if self.instance.city:
        #     self.fields['district'].queryset = District.objects.filter(parent_code=self.instance.city)
        # if self.instance.district:
        #     self.fields['ward'].queryset = Ward.objects.filter(parent_code=self.instance.district)


class AddAvatar(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['avatar']
        labels = {'avatar':'Chọn ảnh đại diện:'}
        widgets = {
            'avatar': forms.FileInput(attrs={'class':'form-control'}),
        }

class UpdateUser(UserInformationForm):
    
    username = forms.CharField(label='Tên tài khoản:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email=forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))

class Add_review(forms.ModelForm):
    class Meta:
        model = Review
        fields =['rating','review']
        labels = {'rating':'Đánh giá', 'review':'Bình luận'}
        widgets ={
            'rating': forms.Select(attrs={'class':'form-control'}),
            'review': forms.Textarea(attrs={'class':'form-control'})
        }
class ContactForm(forms.Form):
    name = forms.CharField(label='Tên của bạn', max_length=255)
    number = forms.CharField(label='Số điện thoại')
    email = forms.EmailField(label='Địa chỉ email của bạn')
    message = forms.CharField(label='Nội dung', widget=forms.Textarea)
    # widgets = {
    #     'name': forms.TextInput(atttrs={'class':'form-control'})
    #     'number': forms.TextInput(atttrs={'class':'form-control'})
    #     'email': forms.TextInput(atttrs={'class':'form-control'})
    #     'message': forms.Textarea(atttrs={'class':'form-control'})
    # }