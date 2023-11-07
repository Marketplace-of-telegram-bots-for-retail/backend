from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

from core.models import TimestampedModel


def user_directory_path(instance, filename):
    return f'users/{instance.id}/{filename}'


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
        extra_fields.setdefault('username', email.split('@')[0])
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
    photo = models.ImageField(
        verbose_name='Фотография пользователя',
        upload_to=user_directory_path,
        blank=True,
        null=True,
    )
    is_seller = models.BooleanField(default=False)

    objects = CustomUserManager()

    def set_username(self):
        self.username = self.email.split('@')[0]

    def __str__(self):
        return self.email


class Seller(TimestampedModel):
    '''Модель продавца.'''

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    inn = models.CharField(
        max_length=12,
        validators=[RegexValidator(r'^[\d+]{10,12}$')],
    )

    class Meta:
        verbose_name = 'продавец'
        verbose_name_plural = 'продавцы'
        ordering = ('-created',)

    def __str__(self):
        return self.user.email
