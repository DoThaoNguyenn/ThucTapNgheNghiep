from django.db import models
from django.contrib.auth.models import AbstractUser
# from .managers import CustomUserManager
# from django.utils.translation import ugettext_lazy as _

from product.models import Product

# Create your models here.
class Users(AbstractUser):
    
    phone = models.CharField(max_length=10,null=True, blank=True)
    address = models.CharField(max_length=255,null=True, blank=True)

    class Meta:
        db_table = 'auth_user'


class Order(models.Model):

    paymentmenthod_choices = (
        (1, "Cash"),
        (2, "Credit card"),
        (3, "Bank transfer"),
    )
    status_choices = (
        (1, "Cart"),
        (2, "Ordered"),
        (3, "Cancelled"),
        
    )
    menthod = models.IntegerField(choices=paymentmenthod_choices, default=1)
    note = models.TextField(max_length=200, null=True, blank=True)
    total = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(Users, related_name='users', on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(choices=status_choices, default=1)

class Order_detail(models.Model):
    order = models.ForeignKey(Order, related_name='order',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_pr',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total(sefl):
        return sefl.quantity*sefl.product.discount_cost()