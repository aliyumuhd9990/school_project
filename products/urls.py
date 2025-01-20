from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexViews, name='index'),
]
