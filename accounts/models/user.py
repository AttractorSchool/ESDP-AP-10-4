from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False, max_length=320)
    is_guide = models.BooleanField(null=False, default=False)
    is_tourist = models.BooleanField(null=False, default=False)
    birthdate = models.DateField(null=True, blank=False)
    encrypted_card_token = models.CharField(max_length=255, null=True, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
