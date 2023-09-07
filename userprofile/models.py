from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='img/profile_pictures', blank=True, null=True)
    shipping_address = models.TextField(blank=True)
    billing_address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=80, blank=True, unique=True)
    
    def __str__(self):
        return self.user.username

