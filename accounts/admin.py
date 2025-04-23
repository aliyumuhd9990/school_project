from django.contrib import admin
from.models import *

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'full_name', 'role', 'last_login', 'password'
    ]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'profile_img', 'contact'
    ]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'state', 'city', 'street'
    ]

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    pass



# admin.site.register(CustomUser)

