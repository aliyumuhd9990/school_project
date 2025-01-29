from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'crop_price', 'crop_desc', 'crop_img')


