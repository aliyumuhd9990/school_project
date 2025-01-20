from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupViews, name='signup'),
    path('login/', LoginViews, name='login'),
]
