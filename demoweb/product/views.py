from django.shortcuts import render
from django.http import HttpResponse
from .models import category, product, product_information

# Create your views here.
def index(request):
    ds = category.objects.all()
    sp = product.objects.all()
   
    
    return render(request, 'product/index.html', {'loaisp':ds, 'sanpham':sp})

def detail(request, id):
    
    lsp = category.objects.get(pk=id)
    sp = product.objects.filter(category=id)
    return render(request, "product/detail.html", {'sanpham':sp,'loaisp':lsp})
    
def infor(request, id):
    sp = product.objects.get(pk=id)
    inf = product_information.objects.filter(product=id)
    return render(request,"product/product_detail.html", {'sp':sp,'information':inf})
