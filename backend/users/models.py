# from products.models import Product
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TimestampedModel


class User(AbstractUser, TimestampedModel):
    email = models.EmailField(
        'адрес электронной почты',
        unique=True,
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
    phone = models.CharField(max_length=20)
    is_bayer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    # favorites = models.ManyToManyField(
    #     Product, blank=True, default=False, related_name="favorites"
    # )

    def __str__(self):
        return self.email
