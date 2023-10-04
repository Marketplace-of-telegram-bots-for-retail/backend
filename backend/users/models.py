from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from core.models import TimestampedModel


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', email)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, TimestampedModel):
    '''Кастомная модель пользователя.'''

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(
        'адрес электронной почты',
        unique=True,
        max_length=200,
    )
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(
        'имя',
        max_length=50,
        blank=False,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=50,
        blank=False,
    )
    phone = models.CharField(
        'номер телефона',
        max_length=20,
        blank=False,
    )
    is_bayer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    objects = CustomUserManager()

    def set_username(self):
        self.username = self.email

    def __str__(self):
        return self.email
