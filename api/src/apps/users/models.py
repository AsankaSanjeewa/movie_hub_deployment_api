from django.db import models
from django.contrib.auth.models import AbstractUser


class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False, verbose_name="email", max_length=255)
    imageUrl = models.ImageField(upload_to='profile/', blank=True, null=True)
    first_name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(blank=True, max_length=100)

    EMAIL_FIELD = "email"
    # USERNAME_FIELD = 'username'
