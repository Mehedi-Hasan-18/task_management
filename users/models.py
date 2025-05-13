from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
"""class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='userprofile',on_delete=models.CASCADE, primary_key=True)
    profile_img = models.ImageField(upload_to='profile_image', blank=True)
    bio = models.TextField(blank=True)
    
    
    def __str__(self):
        return self.user.username"""
    
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_image', blank=True,default='profile_image/Screenshot_2023-11-17_003842.png')
    
    def __str__(self):
        return self.username