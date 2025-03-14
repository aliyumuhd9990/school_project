from django.db import models
from accounts.models import *
from products.models import *
# from django.conf import settings

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email if self.user else 'Guest'}"

    def __itr__(self):
        for item in self.cart.values():
            yield item

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def clear(self):
       self.items.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2, default=True)

    def __str__(self):
        return f"{self.quantity} x {self.crop.crop_name} in {self.cart.user.email}'s cart"
    
    def __itr__(self):
        for item in self.cart.values():
            yield item

    def total_price(self):
        return self.quantity * self.crop.crop_price  # Assuming your Product model has a price field
