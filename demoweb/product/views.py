from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from .models import Category, Product,Review
from order.models import Order, Users, Order_detail,Contact
from .forms import Product_create_form, Category_create_form, Register_form,UserInformationForm,AddAvatar,UpdateUser,Add_review,ContactForm
from vi_address.models import City, District, Ward
from django.core.paginator import Paginator
from django.contrib import messages,sessions
from django.urls import reverse

from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime, timedelta
from django.core.mail import send_mail,BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
# Create your views here.
def index(request):
    ds = Category.objects.all()
    return render(request, 'product/index.html', {'loaisp':ds})

def detail(request, id):
    
    lsp = Category.objects.all()
    sp = Product.objects.filter(category=id)
    return render(request, "product/detail.html", {'sanpham':sp,'loaisp':lsp})
    
def infor(request, id):
    sp = Product.objects.get(pk=id)
    avg_rating=[]
    x=sp.rating()
    for i in range(5):
        if x >= 1: avg_rating += [1]
        elif x >= 0.5: avg_rating += [2]
        else: avg_rating += [3]
        x -= 1
    if request.user.is_authenticated:
        form = Add_review
        if Review.objects.filter(user=request.user,product=sp).count()>0:
            message = 'Khách hàng đã đánh giá sản phẩm này !'
            is_review = False
            
        else: 
            is_review = True
            message = ""
            if request.method == 'POST':
                form = Add_review(request.POST)
                if form.is_valid():
                    new_review = Review.objects.create(
                        user = request.user,
                        product = sp,
                        created_time = timezone.now(),
                        rating = request.POST.get('rating'),
                        review = request.POST.get('review')
                    )
                else:
                    print(form.errors.as_data())
        return render(request,"product/product_detail.html", {'sp':sp,'form':form,'is_review':is_review,'message':message, 'avg_rating':avg_rating,})
    else:
        login_message = "Vui lòng đăng nhập để có thể đánh giá sản phẩm !"
    return render(request,"product/product_detail.html", {'sp':sp,'login_message':login_message})


def create_product(request):
    pr = Product_create_form()
    if request.method=="POST":
        print(request.POST)
        pr=Product_create_form(request.POST, request.FILES)
        if pr.is_valid():
            pr.save()
            return HttpResponse("Save success")
        else:
            print(pr.errors.as_data())
            return render (request, template_name="product/create_product.html",context={'pr':pr})   
    return render(request,'product/create_product.html',{'pr':pr})


def list_product(request):
    sp=Product.objects.all()
    s= []
    for i in range(1,sp.count()):
        s += [i]

    return render (request, 'product/list_product.html',{'sp':sp,'s':s})



def update_product(request, id):
    sp = Product.objects.get(pk=id)
    pr = Product_create_form(instance=sp)
    if request.method=="POST":
        pr=Product_create_form(request.POST, request.FILES, instance=sp)
        if pr.is_valid():
            pr.save()
            return HttpResponse("Update success")
        else:
            return HttpResponse('Fail')
    return render (request, 'product/create_product.html',{'sp':sp,'pr':pr})


def delete_product(request, id):
    sp = Product.objects.get(pk=id)
    if request.method=="POST":
        sp.delete()
        return redirect('/list_product/')
    return render (request, 'product/delete_product.html',{'sp':sp})


# def add_product_information(request,id):
#     form = Add_Product_information()
#     sp=Product.objects.get(pk=id)
#     if request.method == 'POST':
#         form = Add_Product_information(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse ('Add information success')
#         else:
#             print(form.errors.as_data())

#     return render(request, 'product/add_product_information.html',{'form':form})



def list_category(request):
    lsp=Category.objects.all()
    return render (request, 'product/list_category.html',{'lsp':lsp})



def create_category(request):
    form=Category_create_form()
    if request.method=="POST":
        form=Category_create_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('Success')
        else:
            print(form.errors.as_data())
            return HttpResponse('Fail')
    return render(request, 'product/create_category.html', context={'form':form})

def update_category(request, id):
    category = Category.objects.get(pk=id)
    form = Category_create_form(instance=category)
    if request.method=="POST":
        print(request.POST)
        category=Category_create_form(request.POST, request.FILES, instance=category)
        if form.is_valid():
           
            form.save()
            return HttpResponse("Update success")
        else:
            return HttpResponse('Fail')
    return render (request, 'product/create_category.html',{'category':category,'form':form})

def delete_category(request, id):
    category = Category.objects.get(pk=id)
    if request.method=="POST":
        category.delete()
        return redirect('/list_category/')
    return render (request, 'product/delete_category.html',{'category':category})


def register(request):
    form = Register_form()

    if request.method == 'POST':
        form=Register_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request,'product/register.html',{'form':form})

# def show_question(request):
#     form_question=Question()
#     return render(request,'product/show_question.html',{'form_question1':form_question})

def add_to_cart(request,id):

    
    user = request.user
    if user.is_authenticated:

        product = Product.objects.get(pk=id)   
        order, created = Order.objects.get_or_create(user = request.user, status =1)
        orderdetail, created1 = Order_detail.objects.get_or_create(order = order, product = product)
        if not created1:
            orderdetail.quantity += 1
            orderdetail.save()

        orderDetail = Order_detail.objects.filter(order=order) 
        request.session['count_cartitem'] = orderDetail.count()

        return redirect(reverse(viewname='product:information', args=[id]))
        
    else:
        return redirect('product:login')

def remove_orderDetail(request, id):
    item = Order_detail.objects.get(pk=id)
    item.delete()
    return redirect('product:show_cart')

def show_cart(request):
    if Order.objects.filter(user=request.user, status =1).exists() is False: 
        context ={
            "error_message":  'Chưa có sản phẩm trong giỏ hàng.',
            "is_order": False
        }
        return render(request, 'product/cart.html', context)
    else:
        order = Order.objects.get(user=request.user, status =1)
        orderDetail = Order_detail.objects.filter(order=order)   
        order.quantity = sum(obj.quantity for obj in orderDetail)
        order.total_price = sum(obj.product.discount_cost()*obj.quantity for obj in orderDetail)
        order.save()

        request.session['count_cartitem'] = orderDetail.count()
        context = {
            'orderDetail':orderDetail,
            'order':order,
            "is_order": True
        }
        return render (request, 'product/cart.html',context)
        

def checkout(request):

    user = Users.objects.get(pk=request.user.pk)
    order = Order.objects.get(user=user, status = 1)
    orderdetail = Order_detail.objects.filter(order=order)    
    form_user = UserInformationForm(instance=user)
    return render(request, 'product/checkout.html',{'form_user':form_user,'orderdetail':orderdetail,'order':order})



def minus_quantity(request,id):
    item = Order_detail.objects.get(pk=id)
    if item.quantity == 1:
        item.delete()
    else:
        item.quantity -= 1
        item.save()
    print(item.quantity)
    return redirect('product:show_cart')

def plus_quantity(request,id):
    item = Order_detail.objects.get(pk=id)
    item.quantity += 1
    item.save()
    print(item.quantity)
    return redirect('product:show_cart')


def review_order(request,id):
    order = Order.objects.get(pk=id)
    orderdetail = Order_detail.objects.filter(order=order)
    
    return render(request, 'product/review_order.html', {'order':order,'orderdetail':orderdetail})


def order_list(request):
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(pk=order_id)
        form_user = UserInformationForm(request.POST,instance=Users.objects.get(pk=request.user.pk))
        if form_user.is_valid():
            form_user.save()
            order.datetime = timezone.now()
            order.status = 2
            del request.session['count_cartitem']
        else:
            print(form_user.errors.as_data())
        order.save()
    # lọc đơn hàng theo thời gian:
    get_startdate = request.GET.get('start_date')
    get_enddate = request.GET.get('end_date')
    if get_startdate and get_enddate:
        startdate = datetime.strptime(get_startdate, '%Y-%m-%d')
        enddate = datetime.strptime(get_enddate, '%Y-%m-%d') + timedelta(days=1)

        #lọc:
        orders_filtered = Order.objects.filter(datetime__range=(startdate, enddate))
        
        return render(request,'product/order_list.html',{'orders_filtered':orders_filtered})
    list = Order.objects.filter(user=request.user, status =2)
    return render (request,'product/order_list.html',{'order':list})
      



# trang product
def product_list(request):
    loaisp = Category.objects.all()
    sp = Product.objects.all()
    paginator = Paginator(sp,10) # mỗi trang hiển thị 1 đối tượng
    page= request.GET.get('page')
    page_obj = paginator.get_page(page)
    nums="a" * page_obj.paginator.num_pages
    # lọc sản phẩm theo giá:
    mincost = request.GET.get('min_cost')
    maxcost = request.GET.get('max_cost')
    if mincost and maxcost:
        product_filtered = Product.objects.filter(cost__range=(mincost,maxcost))
        return render(request,'product/product_list.html',{'loaisp': loaisp,'product_filtered':product_filtered})
    return render(request,'product/product_list.html',{'loaisp': loaisp,'sp': sp,'page_obj': page_obj,'nums':nums})
    
#hien sản phẩm khi click vào sidebar
def product_select_main(request, id):
    lsp = Category.objects.all()
    sp = Product.objects.filter(category=id)
    paginator = Paginator(sp,5) # mỗi trang hiển thị 1 đối tượng
    page= request.GET.get('page')
    page_obj = paginator.get_page(page)
    nums="a" * page_obj.paginator.num_pages
    # return render(request, 'product/product.html', {})
    return render(request, "product/product.html", {'sanpham':sp,'loaisp':lsp,'page_obj': page_obj,'nums':nums})
#dhien ds loai sp sidebar
def product_select(request):
    lsp = Category.objects.all()
    return render(request, "product/product.html", {'loaisp':lsp})
# (modifié) 
# trang about us
def about_us(request):
    return render(request,"product/aboutus.html")
# trang contact
def contact(request):
    return render(request,"product/contact.html")
def search(request):
    q=request.GET.get('q')
    q.lower()
    query=q.split()
    print(query)
    # if len(query)==1:
    #     sp=Product.objects.filter(title__icontains=query[0])
    # elif len(query)==2:
    #     sp=Product.objects.filter(Q(title__icontains=query[0]) | 
    #     Q(title__icontains=query[1]) )
    # elif len(query)==3:
    #     sp=Product.objects.filter(Q(title__icontains=query[0]) | 
    #     Q(title__icontains=query[1]) | 
    #     Q(title__icontains=query[2]) )
    # elif len(query)==4:
    #     sp=Product.objects.filter(Q(title__icontains=query[0]) | 
    #     Q(title__icontains=query[1]) | 
    #     Q(title__icontains=query[2])| 
    #     Q(title__icontains=query[3]) )
    # elif len(query)==5:
    #     sp=Product.objects.filter(Q(title__icontains=query[0]) | 
    #     Q(title__icontains=query[1]) | 
    #     Q(title__icontains=query[2]) | 
    #     Q(title__icontains=query[3]) | 
    #     Q(title__icontains=query[4]) 
    #     ) 
    queries = [Q(title__icontains=query) for query in query]
    query1 = queries.pop()
    for item in queries:
        query1 |= item
    sp = Product.objects.filter(query1)
    return render(request,"product/search.html",{'sp':sp})
# password_change_form
class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for fieldname  in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].widget.attrs={ 'class': 'form-control'}




# load districts:
def load_districts(request):
    city_id = request.GET.get('city')
    districts = District.objects.filter(parent_code=city_id)
    return render(request, 'product/district_option.html',{'districts':districts})

def load_wards(request):
    district_id = request.GET.get('district')
    wards = Ward.objects.filter(parent_code=district_id)
    return render(request, 'product/ward_option.html',{'wards':wards})

def profile(request):
    user = Users.objects.get(pk=request.user.pk)
    form = AddAvatar
    form_update = UpdateUser
    if request.method == 'POST':
        form = AddAvatar(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    if request.method == 'POST' and 'username' in request.POST:
        form_update = UpdateUser(request.POST, instance=user)
        if form_update.is_valid():
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            form_update.save()
        else:
            print(form_update.errors.as_data())
    return render(request, 'product/profile.html',{'user':user,'form_update':form_update,'form':form})



    
# trang contact
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = Contact(
                name=form.cleaned_data['name'],
                number=form.cleaned_data['number'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            contact.save()
            return render(request, 'product/contact_label.html')
    else:
        form = ContactForm()

    return render(request, 'product/contact.html', {'form': form})

# lọc đơn hàng theo thời gian:
# def filter_order(request):
#     get_startdate = request.GET.get('start_date')
#     get_enddate = request.GET.get('end_date')
#     if get_startdate and get_enddate:
#         startdate = datetime.strptime(get_startdate, '%Y-%m-%d')
#         enddate = datetime.strptime(get_enddate, '%Y-%m-%d')

#         #lọc:
#         orders_filtered = Order.objects.filter(datetime__range=(startdate, enddate))
#         return render(request,'product/account.html',{'orders_filtered':orders_filtered})
#     order = Order.objects.all()
#     return render(request, 'product/account.html', {'order': order})
#View password

# accounts/views.py

# from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
# from .forms import CustomPasswordResetForm


# class CustomPasswordResetView(PasswordResetView):
#     form_class = CustomPasswordResetForm
#     template_name  'product/forgot_password.html'
#     success_url '/product/forgot-password/done/'


# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name  'product/reset_password.html'
#     success_url  '/product/reset-password/complete/'
# forgot_password  CustomPasswordResetView.as_view()
# reset_password  CustomPasswordResetConfirmView.as_view()
# def password_reset_request(request):
#     if request.method == 'POST':
#         password_form = PasswordResetForm(request.POST)
#         if password_form.is_valid():
#             data = password_form.cleaned_data['email']
#             user_email=Users.objects.filter(Q(email=data))
#             user=user_email.first()
#             print(user.email)
#             if user_email.exists():
#                 for user in user_email:
#                     subject = 'Password Request'
#                     email_template_name = 'product/password_message.txt'
#                     parameters = {
#                         'email': user.email,
#                         'domain':'127.0.0.1:8000',
#                         'site_name':'PostScribers',
#                         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                         'token': default_token_generator.make_token(user),
#                         'protocol':'http',

#                     }
#                     email= render_to_string(email_template_name,parameters)
#                     print([user.email],11)
#                     try:
#                         send_mail(subject,email,'odooFM2023@gmail.com',[user.email],fail_silently=False)
#                     except:
#                         return HttpResponse('Invalid Header')

#     else:
#         password_form = PasswordResetForm()
#     context={
#         'password_form':password_form,
#     }
#     return render (request,'product/password_reset_form.html',context)
# from django.contrib import messages, auth
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMessage
# def forgotPassword(request):

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         print(email)
#         user = Users.objects.get(email__exact=email)
  
#         current_site = get_current_site(request=request)
#         mail_subject = 'Reset your password'
#         message = render_to_string('product/reset_password_email.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': default_token_generator.make_token(user)
#         })
#         # send_email = EmailMessage(mail_subject, message, to=[email])
#         # send_email.send()
#         send_mail(mail_subject,message,'',[email],fail_silently=False)

#         messages.success(
#             request=request, message="Password reset email has been sent to your email address")
#     else:
#         messages.error(request=request, message="Account does not exist!")

#     context = {
#         'email': email if 'email' in locals() else '',
#     }
#     return render(request, "product/forgot_password.html", context=context)


# def reset_password_validate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = Users.objects.get(pk=uid)
#     except Exception:
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         request.session['uid'] = uid
#         messages.info(request=request, message='Please reset your password')
#         return redirect('reset_password')
#     else:
#         messages.error(request=request, message="This link has been expired!")
#         return redirect('home')


# def reset_password(request):
#     if request.method == 'POST':
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')

#         if password == confirm_password:
#             uid = request.session.get('uid')
#             user = Users.objects.get(pk=uid)
#             user.set_password(password)
#             user.save()
#             messages.success(request, message="Password reset successful!")
#             return redirect('login')
#         else:
#             messages.error(request, message="Password do not match!")
#     return render(request, 'product/reset_password.html')

from django.contrib import messages

def forgot_password_question(request):
    if request.method == 'POST':
        username = request.POST['username']
        answer = request.POST['answer']
        question = request.POST['question']
        try:
            user = Users.objects.get(username=username)
            if user.question and user.answer:
                if answer == user.answer :
                    # Cung cấp câu trả lời khớp, cho phép người dùng nhập mật khẩu mới
                    return redirect('product:reset_password_question', user_id=user.id)
                else:
                    # Câu trả lời không khớp
                    messages.error(request, 'Câu trả lời không đúng.')
            else:
                # Người dùng không có câu hỏi xác thực
                messages.error(request, 'Người dùng không có câu hỏi xác thực.')
        except User.DoesNotExist:
            # Người dùng không tồn tại
            messages.error(request, 'Người dùng không tồn tại.')

    return render(request, 'product/forgot_password_question.html')
from django.contrib.auth.hashers import make_password

def reset_password_question(request,user_id):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:
            user = Users.objects.get(id=user_id)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Mật khẩu đã được thay đổi thành công.')
            return redirect('product:login')
        else:
            messages.error(request, 'Xác nhận mật khẩu không khớp.')

    return render(request, 'product/reset_password_question.html', {'user_id': user_id})