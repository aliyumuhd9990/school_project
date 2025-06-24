from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
# from allauth.account.views import 

urlpatterns = [
    path('signup/', SignupView, name='signup'),
    path('login/', LoginView , name='login'),
    path('farmer-login/', FarmerLoginViews, name='farmer-login'),
    path('logout/', logoutView, name='logout'),
    path('user-account/', AccountView, name='account'),
    path('edit-profile/', EditProfileView, name='edit-profile'),
    path('edit-address/', EditAddressView, name='edit-address'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name= 'accounts/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name= 'accounts/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name= 'accounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name= 'accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name= 'accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name= 'accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('email_sent/', SentEmailView, name='email_sent'),
    path('email_verification/<uidb64>/<token>/', ActivateEmailView, name='activate'),
]
