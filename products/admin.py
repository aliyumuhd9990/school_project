from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Category)
class CategotyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'slug', 'crop_price', 'available', 'created', 'updated')
    list_filter = ['available', 'created', 'updated']
    list_editable = ['crop_price', 'available']
    prepopulated_fields = {'slug': ('crop_name',)}


