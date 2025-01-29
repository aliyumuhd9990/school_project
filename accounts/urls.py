from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupViews, name='signup'),
    path('login/', LoginViews, name='login'),
    path('logout/', logoutView, name='logout'),
    path('farmer-signup/', FarmerSignupViews, name='farmer-signup'),
    path('farmer-login/', FarmerLoginViews, name='farmer-login'),
    path('farmer-logout/', FarmerLogoutView, name='farmer-logout'),
]
