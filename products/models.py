from django.db import models
from django.urls import reverse
from accounts.models import CustomUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product:products-list-by-category', args=[self.slug])
    

class Crop(models.Model):
    farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'farmer'})
    category = models.ForeignKey(Category, related_name='crops', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, db_index=True)
    crop_name = models.CharField(max_length=100)
    crop_price = models.DecimalField(max_digits=10, decimal_places=2)
    crop_desc = models.TextField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    crop_img = models.ImageField(upload_to='img/products_img', height_field=None, width_field=None, max_length=100)

    class Meta:
        ordering = ('crop_name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.crop_name
    
    def get_absolute_url(self):
        return reverse('product:product-detail', args=[self.id, self.slug])
    

