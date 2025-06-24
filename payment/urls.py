from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('initialize/<int:order_id>/', views.initialize_payment, name='initialize_payment'),
    path('verify/', views.verify_payment, name='verify_payment'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]