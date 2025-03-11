from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['crop']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'city', 'location', 'paid', 'created', 'updated']

    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInLine]
