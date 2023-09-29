from django.db import models

from django.contrib.auth.models import AbstractUser
from products.models import Product
from abstract_models.models import AbstractBaseModel 


class User(AbstractUser, AbstractBaseModel):
    """Кастомная модель пользователя"""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(
        unique=True,
        verbose_name="Адрес электронной почты",
        max_length=200,
    )
    first_name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name="Фамилия",
    )
    phone  = models.CharField(
        max_length=20,
        blank=False,
        verbose_name="Номер телефона",
    )
    is_bayer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    
    
    def set_username(self):
        self.username = self.email
    

    def __str__(self):
        return self.email
