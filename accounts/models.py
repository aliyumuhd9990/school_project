from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (('user','User'), ('farmer', 'Farmer'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Other required fields apart from email

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    contact = models.IntegerField(blank=True, null=True)
    profile_img = models.ImageField(upload_to='img/profile_images', default='img/profile_images/du.png', blank=True, null=True)


    def __self__(self):
        return self.user.email
    

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_user = models.IntegerField(blank=True, null=True)
    state = models.CharField(default="Kano", max_length=50)
    city = models.CharField(default="Kumbotso", max_length=50)
    street = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, default=True)
