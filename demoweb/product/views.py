from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Product, Product_information
from order.models import Order
from .forms import Product_create_form
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

def add_to_cart(request, id):
    print(23232)
    a=Product.objects.get(pk=id)
    print(a)
    b=Order.objects.get(pk=1)
    b.product.add(a)
    print(b)
    b.save()
    return HttpResponse("Thêm vào giỏ hàng thành công !")


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
        pr=Product_create_form(request.POST)
        if pr.is_valid():
            print('7777777')
            pr.save()
            return HttpResponse("Save success")
        else:
            return HttpResponse('Fail')   
    return render(request,'product/create_product.html',{'pr':pr})


