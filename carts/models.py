from django.db import models
from accounts.models import *
from products.models import *

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.crop.crop_price
    
    def __str__(self):
        return f"{self.quantity} x {self.crop.crop_name} ({self.user.username})"
