from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from .models import Category, Product, Product_information
from order.models import Order, Users, Order_detail
from .forms import Product_create_form, Category_create_form, Register_form, Add_Product_information,UserInformationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse


# Create your views here.
def index(request):
    ds = Category.objects.all()
    sp = Product.objects.all()
   
    
    return render(request, 'product/index.html', {'loaisp':ds, 'sanpham':sp})

def detail(request, id):
    
    lsp = Category.objects.all()
    sp = Product.objects.filter(category=id)
    return render(request, "product/detail.html", {'sanpham':sp,'loaisp':lsp})
    
def infor(request, id):
    sp = Product.objects.get(pk=id)
    inf = Product_information.objects.get(product=id)
    
    return render(request,"product/product_detail.html", {'sp':sp,'information':inf})




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
    return render (request, 'product/list_product.html',{'sp':sp})



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


def add_product_information(request,id):
    form = Add_Product_information()
    sp=Product.objects.get(pk=id)
    if request.method == 'POST':
        form = Add_Product_information(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse ('Add information success')
        else:
            print(form.errors.as_data())

    return render(request, 'product/add_product_information.html',{'form':form})



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
        else:
            print(form_user.errors.as_data())
        order.save()
    list = Order.objects.filter(user=request.user, status =2)
    return render (request,'product/account.html',{'order':list})
      



# trang product
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
    sp=Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request,"product/search.html",{'sp':sp})
