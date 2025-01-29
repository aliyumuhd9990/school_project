from django.contrib import admin
from.models import CustomUser, Profile

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'full_name',  'last_login', 'password'
    ]
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'profile_img',  'location', 'state', 'city', 'contact'
    ]



# admin.site.register(CustomUser)

