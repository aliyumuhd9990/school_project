from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('kbt_marketplace_administration/', admin.site.urls),
    path('auth/', include('allauth.urls')),  # allauth URLs
    path('accounts/', include('accounts.urls')),
    path('cart/', include('carts.urls')),
    path('order/', include('orders.urls', namespace='orders')),
    path('', include('products.urls', namespace='products')),
    path('payment/', include(('payment.urls','payment'), namespace='payment')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

