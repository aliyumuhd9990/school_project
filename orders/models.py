from django.db import models
from products.models import *
from carts.models import *

# Create your models here.
class Order(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    city = models.CharField(max_length=50)
    contact = models.IntegerField()
    location = models.CharField(max_length=250, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.cart_items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        self.price = self.crop.crop_price * self.quantity

        super().save(*args, **kwargs)
    def get_cost(self):
        return self.price * self.quantity

