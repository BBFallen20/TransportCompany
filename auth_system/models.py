from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=50, verbose_name='Email', unique=True)
    password = models.CharField(max_length=16, validators=[MinLengthValidator(8)], verbose_name='Password')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
