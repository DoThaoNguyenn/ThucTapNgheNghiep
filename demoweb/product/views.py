from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from .models import Category, Product, Product_information
from order.models import Order, Users, Order_detail
from .forms import Product_create_form, Category_create_form, Register_form, Add_Product_information,UserInformationForm, OrderForm
from django.core.exceptions import ObjectDoesNotExist

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
            print('7777777')
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
        print(request.POST)
        pr=Product_create_form(request.POST, request.FILES, instance=sp)
        if pr.is_valid():
            print('7777777')
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
    print(2222)
    if user.is_authenticated:
        product = Product.objects.get(pk=id)   
        order, created = Order.objects.get_or_create(user = request.user, status =1)
        orderdetail, created1 = Order_detail.objects.get_or_create(order = order, product = product)
        if not created1:
            orderdetail.quantity += 1
            orderdetail.save()

        
    
        return redirect('product:show_cart')
    else:
        return redirect('product:login')

def remove_orderDetail(request, id):
    item = Order_detail.objects.get(pk=id)
    item.delete()
    return redirect('product:show_cart')

def show_cart(request):
    print(343333)

    if Order.objects.filter(user=request.user, status =1).exists() is False: 
        # error_message = 'Chưa có sản phẩm trong giỏ hàng.'
        context ={
            "error_message":  'Chưa có sản phẩm trong giỏ hàng.',
            "is_order": False
        }
        return render(request, 'product/cart.html', context)
    else:
        order = Order.objects.get(user=request.user, status =1)
        orderDetail = Order_detail.objects.filter(order=order)   
        order.quantity = sum(obj.quantity for obj in orderDetail)
        order.total = sum(obj.product.discount_cost()*obj.quantity for obj in orderDetail)
        order.save()

        context = {
            'orderDetail':orderDetail,
            'order':order,
            "is_order": True
        }
        return render (request, 'product/cart.html',context)
        

def checkout(request):

    user = Users.objects.get(pk=request.user.pk)
    print(11, user)
    order = Order.objects.get(user=user, status = 1)
    print(22, order)
    orderdetail = Order_detail.objects.filter(order=order)
    print(999, orderdetail)
    form_user = UserInformationForm(instance=user)
    form_order = OrderForm(instance=order)
    if request.method == 'POST':
        form_user = UserInformationForm(request.POST,instance=user)
        form_order = OrderForm(request.POST,instance=order)
        if form_user.is_valid():
            form_order.save()
            form_user.save()
        else:
            print(form_user.errors.as_data())
            print(form_order.errors.as_data())
    return render(request, 'product/checkout.html',{'form_user':form_user,'form_order':form_order,'orderdetail':orderdetail,'order':order})



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


def review_order(request):
    
    order_id = request.POST.get('order_id')
    order = Order.objects.get(pk=order_id)
    print(order)
    orderdetail = Order_detail.objects.filter(order=order)
    if request.method == 'POST':
        order.datetime = timezone.now()
        order.status = 2
    order.save()
    return render(request, 'product/review_order.html', {'order':order,'orderdetail':orderdetail})