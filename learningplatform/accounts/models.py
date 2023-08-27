from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=120, blank=True, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('Subject', related_name='user_profiles', blank=True)

    def __str__(self):
        return self.user.username

class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name