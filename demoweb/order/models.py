from django.db import models
from django.contrib.auth.models import AbstractUser
# from .managers import CustomUserManager
# from django.utils.translation import ugettext_lazy as _

from product.models import Product

# Create your models here.
class Users(AbstractUser):
    # username = None
    # email = models.EmailField(_('email address'), unique=True)
    # name= models.CharField(_("full name"), max_length=100)
    # address = models.CharField(max_length=200)
    # phone = models.CharField(_("phone number"), max_length=10)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    # objects = CustomUserManager()

    # def __str__(self):
    #     return self.name
    pass



class Order(models.Model):

    paymentmenthod_choices = (
        (1, "Cash"),
        (2, "Credit_card"),
        (3, "Electronic_bank_transfer"),
    )
    menthod = models.IntegerField(choices=paymentmenthod_choices, default=1)
    note = models.CharField(max_length=200, null=True, blank=True)
    total = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(Users, related_name='users', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Product, related_name='products_order')

    
class Cart(models.Model):
    users=models.ForeignKey(Users, related_name='user', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='product',on_delete=models.CASCADE,null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    
