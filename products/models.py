from django.db import models
from django.urls import reverse
from accounts.models import CustomUser
from django.utils.text import slugify

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
        return reverse('products:products-list-by-category', args=[self.slug])
    

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
        return reverse('products:products-detail', args=[self.id, self.slug])
        # return reverse('product-detail', kwargs={'category_name': self.category})
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.crop_name)
            counter = 1
            original_slug = self.slug
            
            while Crop.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class withdrawalRequest(models.Model):
    farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'farmer'})
    bank_name = models.CharField(max_length = 150)
    account_name = models.CharField(max_length = 150)
    account_num = models.CharField(max_length = 150)
    withdrawal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.bank_name
    
    
    

    

