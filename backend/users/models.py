from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TimestampedModel


class User(AbstractUser, TimestampedModel):
    '''Кастомная модель пользователя.'''

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(
        'адрес электронной почты',
        unique=True,
        max_length=200,
    )
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

    def set_username(self):
        self.username = self.email

    def __str__(self):
        return self.email
