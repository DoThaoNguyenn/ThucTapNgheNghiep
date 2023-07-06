from django.db import models
from django.utils import timezone

# Create your models here.
class categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class products(models.Model):
    

    category = models.ForeignKey(categories, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.IntegerField()
    quantity = models.IntegerField()
    discount = models.FloatField()
    image = models.ImageField()

    def __str__(self):
        return self.name


class orders(models.Model):
    status_choices = (
        (1, ("Processing")),
        (2, ("Shipping")),
        (3, ("Completed")),
    )

    status = models.IntegerField(choices=status_choices, default=1)
    total_money = models.IntegerField(default=0)
    total_product = models.IntegerField(default=0)
    customer_name = models.CharField(max_length=100, null=False)
    customer_address = models.CharField(max_length=200, null=False)
    customer_phone = models.IntegerField(null=False)

    def __str__(self):
        return self.customer_name

class order_detail(models.Model):
    order = models.ForeignKey(orders, related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey(products, related_name='products', on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)

    # def __str__(self):
    #     return self.quantity

class payments(models.Model):
    paymentmenthods_choices = (
        (1, "Cash"),
        (2, "Credit_card"),
        (3, "Electronic_bank_transfer"),
    )
    order = models.ForeignKey(orders, related_name='order_payment', on_delete=models.CASCADE)
    menthods = models.IntegerField(choices=paymentmenthods_choices, default=1)
    datetime = models.DateTimeField()

    # def __str__(self):
    #     return self.order_payment
