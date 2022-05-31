from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    password = None
    username = None 
    phone_number = models.CharField(max_length=11, unique=True)
        
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'<phone number: {self.phone_number}>'