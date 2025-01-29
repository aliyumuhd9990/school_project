from django.db import models

# Create your models here.
class Crop(models.Model):
    crop_name = models.CharField(max_length=100)
    crop_price = models.IntegerField()
    crop_desc = models.TextField()
    crop_img = models.ImageField(upload_to='img/products_img', height_field=None, width_field=None, max_length=100)
    
    

