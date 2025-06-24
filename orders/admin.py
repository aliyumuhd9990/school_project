from django.contrib import admin
from .models import Order, OrderItem
# from django.urls import reverse
# from django.utils.safestring import mark_safe

# Register your models here.
class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['crop']

@admin.action(description="Approve selected payments")
def approve_payment(modeladmin, request, queryset):
    for order in queryset.filter(status=False):
        order.paid = True
        order.farmer.balance += order.amount  # Update balance
        order.farmer.save()
        order.save()

# def order_pdf(obj):
#     url = reverse('orders:admin_order_pdf', args=[obj.id])
#     return mark_safe(f'<a href="{url}">PDF</a>') 
# order_pdf.short_description = 'Invoice'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'city', 'location', 'paid']
    actions = [approve_payment]

    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInLine]
