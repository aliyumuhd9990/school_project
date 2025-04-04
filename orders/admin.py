from django.contrib import admin
from .models import Order, OrderItem

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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'city', 'location', 'paid', 'created', 'updated']
    actions = [approve_payment]

    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInLine]
