from django.urls import path
from .views import *

urlpatterns = [
    path('cart_view/', CartView, name='cart_view'), 
    path('add/<int:crop_id>/', CartAddView, name='add_to_cart'),
    path('remove/<int:cart_id>/', RemoveFromCart, name='remove_from_cart'), 
    path('update/<int:cart_id>/', UpdateCart, name='update_cart'), 
    path('checkout/', CheckOut, name='checkout'), 
]

