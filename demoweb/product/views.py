from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Category, Product, Product_information
from order.models import Order, Users, Order_detail
from .forms import Product_create_form, Category_create_form, Register_form, Add_Product_information

# Create your views here.
def index(request):
    ds = Category.objects.all()
    sp = Product.objects.all()
   
    
    return render(request, 'product/index.html', {'loaisp':ds, 'sanpham':sp})

def detail(request, id):
    
    lsp = Category.objects.get(pk=id)
    sp = Product.objects.filter(category=id)
    return render(request, "product/detail.html", {'sanpham':sp,'loaisp':lsp})
    
def infor(request, id):
    sp = Product.objects.get(pk=id)
    inf = Product_information.objects.get(product=id)
    return render(request,"product/product_detail.html", {'sp':sp,'information':inf})


def show_cart(request):
    a = Order.objects.get(pk=1)
    sp = a.product.all() 
    listsp=[]
    for i in sp:
        b=Product.objects.get(pk=i.id)
        listsp = listsp + [b]
    return render(request, "product/cart.html", {"sanpham":listsp})  


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
    
    print(request.user.pk)
    user = Users.objects.get(pk=request.user.pk)
    print(id)
    product = Product.objects.get(pk=id)
    order, created = Order.objects.get_or_create(user = user, status =1)
    print(order, created)
    orderdetail, created1 = Order_detail.objects.get_or_create(order = order, product = product)
    print(orderdetail, created1,product, orderdetail.quantity)
    if not created1:
        orderdetail.quantity += 1
        orderdetail.save()
        print(orderdetail.quantity)
    
    return redirect('product:show_cart')

def show_cart(request):
    order = Order.objects.get(user=request.user.pk, status =1)
    orderDetail = Order_detail.objects.filter(order=order)
    print(order.quantity)
    print(order.total)
    product = Product.objects.all()
    for i in orderDetail:
        order.quantity += i.quantity
        order.total += i.product.discount_cost()
    print(order.quantity)
    print(order.total)
    return render (request, 'product/cart.html', {'product':product,'orderDetail':orderDetail,'order':order})

def checkout(request):
    return render(request, 'product/checkout.html')

