from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import category, product, product_information
from .forms import Register_form
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
    print(77, sp)

    inf = product_information.objects.get(product=id)
    print(88, inf)
    return render(request,"product/product_detail.html", {'sp':sp,'information':inf})
def cart(request):
    return render(request,'product/cart.html')
def register(request):
    form=Register_form
    if request.method == "POST":
        form = Register_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request,'product/register.html',{'form':form})