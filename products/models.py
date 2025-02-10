from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Crop(models.Model):
    farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'farmer'})
    crop_name = models.CharField(max_length=100)
    crop_price = models.IntegerField()
    crop_desc = models.TextField()
    crop_img = models.ImageField(upload_to='img/products_img', height_field=None, width_field=None, max_length=100)

    def __str__(self):
        return self.crop_name
    
    

