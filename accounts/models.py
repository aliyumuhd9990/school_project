from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from django.urls import reverse


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (('user','User'), ('farmer', 'Farmer'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Other required fields apart from email

    def __str__(self):
        return self.email


class Profile(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='farmer_profile')
    email_token = models.CharField(max_length=200, default=False)
    is_verified = models.BooleanField(default=False)
    id_user = models.IntegerField()
    contact = models.CharField(max_length=11, default="080xxxxxx")
    profile_img = models.ImageField(upload_to='img/profile_images', default='img/profile_images/du.png', blank=True, null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __self__(self):
        return self.user.email
    
class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_user = models.IntegerField(blank=True, null=False, default=0)
    state = models.CharField(default="Kano", max_length=50)
    city = models.CharField(default="Kumbotso", max_length=50)
    street = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, default="No.123, bus stop, Kano State.")

# class FarmerProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='farmer_profile')
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     total_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)