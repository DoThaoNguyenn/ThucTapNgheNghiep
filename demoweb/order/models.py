from django.db import models
from product.models import product

# Create your models here.
class order(models.Model):
    status_choices = (
        (1, ("Processing")),
        (2, ("Shipping")),
        (3, ("Completed")),
    )

    status = models.IntegerField(choices=status_choices, default=1)
    total_money = models.IntegerField(default=0)
    total_product = models.IntegerField(default=0)
    customer_name = models.CharField(max_length=100)
    customer_address = models.CharField(max_length=200)
    customer_phone = models.IntegerField(null=False)

    def __str__(self):
        return self.customer_name

class order_detail(models.Model):
    order = models.ForeignKey(order, related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey(product, related_name='products', on_delete=models.CASCADE)
    quantity = models.IntegerField()

  

class payment(models.Model):
    paymentmenthod_choices = (
        (1, "Cash"),
        (2, "Credit_card"),
        (3, "Electronic_bank_transfer"),
    )
    order = models.ForeignKey(order, related_name='order_payment', on_delete=models.CASCADE)
    menthod = models.IntegerField(choices=paymentmenthod_choices, default=1)
    note = models.CharField(max_length=200, null=True)
