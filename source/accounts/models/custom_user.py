from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.enum import LocationEnum
from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False, max_length=320),
    avatar = models.ImageField(upload_to="uploads/avatar", blank=True)
    birthdate = models.DateField(blank=False)
    current_location = models.CharField(choices=LocationEnum.choices, max_length=100, blank=False),
    is_guide = models.BooleanField(default=False),
    is_tourist = models.BooleanField(default=False),
    is_email_confirmed = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
