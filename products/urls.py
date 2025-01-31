from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView, name='index'),
    path('about/', AboutView, name='about'),
    path('product/', ProductView, name='products'),
    path('farmer-dash', FarmerDashView, name='farmer-dash'),
    path('crop-details/<int:id>/', FarmerProductView, name='product-details'),
]
