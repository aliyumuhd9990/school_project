from django.urls import path
from .views import *
app_name = 'products'

urlpatterns = [
    path('', IndexView, name='index'),
    path('farmer-dash/', FarmerDashView, name='farmer_dash'),
    path('view-crops/', ViewCrops, name='view_crop'),
    path('removeCrop/<int:id>', removeCrop, name='remove_crop'),
    path('history_view/', historyView, name='history_view'),
    path('order_list/', OrderListView, name='order_list'),
    path('pending_order_list/', PendingListView, name='pending_order_list'),
    path('withdraw/', withdrawView, name='withdraw_page'),
    path('about/', AboutView, name='about'),
    path('products/',  ProductView, name='products'),
    path('products-list/',  ProductListView, name='products-list'),
    path('products-search/',  product_search, name='product_search'),
    path('add-crop/', AddProductView, name='add-crop'),
    path('edit-crop/<int:id>/', EditProductView, name='edit-crop'),
    path('<int:id>/',  ProductDetailView, name='products-detail'),
    path('<slug:category_slug>/',  ProductListView, name='products-list-by-category'),
    path('invoice/<int:invoice_id>/', invoice_detail, name='invoice_detail'),
    path('invoice/<int:invoice_id>/pdf/', invoice_pdf, name='invoice_pdf'),
    # path('crop-details/<int:id>/', FarmerProductView, name='product-details'),
]
