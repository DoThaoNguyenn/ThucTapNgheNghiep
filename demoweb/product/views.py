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
    list = Order.objects.filter(user=request.user, status =2)
    return render (request,'product/account.html',{'order':list})
      



# trang product
def product_list(request):
    loaisp = Category.objects.all()
    sp = Product.objects.all()
    paginator = Paginator(sp,10) # mỗi trang hiển thị 1 đối tượng
    page= request.GET.get('page')
    page_obj = paginator.get_page(page)
    nums="a" * page_obj.paginator.num_pages
    return render(request,'product/product_list.html',{'loaisp': loaisp,'sp': sp,'page_obj': page_obj,'nums':nums})
    
#hien sản phẩm khi click vào sidebar
def product_select_main(request, id):
    lsp = Category.objects.all()
    sp = Product.objects.filter(category=id)
    paginator = Paginator(sp,1) # mỗi trang hiển thị 1 đối tượng
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

