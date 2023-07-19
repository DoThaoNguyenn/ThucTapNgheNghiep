from django.shortcuts import render
from django.http import HttpResponse
from .models import Order, Users, Order_detail
from product.models import Product
# Create your views here.

# def add_to_cart(request,id):
#     a = Users.objects.get(pk=2)
#     b = Cart.objects.get(user=a)
#     cartitem = Cart_item.objects.get(cart=b)
#     product = Product.objects.get(pk=id)
#     cartitem.product.add(product)
#     cartitem.save()
#     return render(request, 'product/cart.html',{'cartitem':cartitem})


