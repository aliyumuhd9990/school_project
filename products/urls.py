from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView, name='index'),
    path('about/', AboutView, name='about'),
    path('products/',  ProductView, name='products'),
    path('product-detail/<int:id>',  ProductDetailView, name='product-detail'),
    path('farmer-dash/', FarmerDashView, name='farmer-dash'),
    path('add-crop/', AddProductView, name='add-crop'),
    # path('crop-details/<int:id>/', FarmerProductView, name='product-details'),
]
