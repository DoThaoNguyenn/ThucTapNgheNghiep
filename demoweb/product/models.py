from django.db import models

# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    def __str__(self):
        return self.name

class product(models.Model):
    category = models.ForeignKey(category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    cost = models.IntegerField()
    quantity = models.IntegerField()
    discount = models.FloatField()
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.title

    def discount_cost(self):
        return self.cost*(1-(self.discount/100))

class product_information(models.Model):
    product = models.ForeignKey(product, related_name='informations', on_delete=models.CASCADE)
    author =  models.CharField(max_length=50)
    pages = models.IntegerField()
    publisher = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.author

