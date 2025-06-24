from django.urls import path
from . views import *

app_name = 'orders'

urlpatterns = [
    path('create/', CreateOrderView, name='create_order'), 
    path('orders/history/', order_history, name='order_history'),
    path('transaction/history/', transaction_history, name='transaction_history'),
    path('invoice/<int:order_id>/', generate_invoice, name='generate_invoice'),
]

