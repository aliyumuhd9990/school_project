from django.urls import path
from .views import *

app_name = 'orders'
urlpatterns = [
    path('create/', CreateOrderView, name='create_order'), 
]

