from django.db import models

from django.contrib.auth.models import AbstractUser
from products.models import Product
from abstract_models.models import AbstractBaseModel 


class User(AbstractUser, AbstractBaseModel):
    email = models.EmailField(
        unique=True,
        verbose_name="Адрес электронной почты",
    )
    first_name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name="фамилия",
    )
    phone  = models.CharField(max_length=20)
    is_bayer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    favorites = models.ManyToManyField(
        Product, blank=True, default=False, related_name="favorites"
    )
    

    def __str__(self):
        return self.email
