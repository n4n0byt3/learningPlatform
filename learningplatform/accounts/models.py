from django.db import models

class User(models.Model):
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=120, blank=True, null=True)

# Create your models here.
