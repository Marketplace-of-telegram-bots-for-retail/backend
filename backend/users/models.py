from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

from core.models import TimestampedModel
from users.validators import BANK_NAME, ORGANIZATION_TYPE_CHOICES


def user_directory_path(instance, filename):
    return f'users/{instance.id}/{filename}'


def seller_directory_path(instance, filename):
    return f'sellers/{instance.id}/{filename}'


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
    REQUIRED_FIELDS = []

    email = models.EmailField(
        'адрес электронной почты',
        unique=True,
        max_length=200,
    )
    username = models.CharField(max_length=30)
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
        'ИНН',
        max_length=12,
        validators=[
            RegexValidator(
                r'^[\d]{10}$|^[\d]{12}$',
                message=(
                    'ИНН состоит из 10 цифр для юридического лица или 12 цифр '
                    'для физического лица!'
                ),
            ),
        ],
    )
    logo = models.ImageField(
        verbose_name='логотип магазина',
        upload_to=seller_directory_path,
        blank=True,
        null=True,
    )
    store_name = models.TextField(
        'название магазина',
        max_length=25,
        blank=True,
        null=True,
    )
    organization_name = models.TextField(
        'название организации',
        max_length=200,
        blank=True,
        null=True,
    )
    organization_type = models.CharField(
        'тип организации',
        max_length=11,
        choices=ORGANIZATION_TYPE_CHOICES,
        blank=True,
        null=True,
    )
    bank_name = models.CharField(
        'название банка',
        max_length=15,
        choices=BANK_NAME,
        blank=True,
        null=True,
    )
    ogrn = models.CharField(
        'ОГРН',
        max_length=15,
        validators=[
            RegexValidator(
                r'^[\d]{13}$|^[\d]{15}$',
                message=(
                    'ОГРН состоит из 13 цифр для юридического лица или '
                    '15 цифр для ИП!'
                ),
            ),
        ],
        blank=True,
        null=True,
    )
    kpp = models.CharField(
        'КПП',
        max_length=9,
        validators=[
            RegexValidator(r'^[\d]{9}$', message='КПП состоит из 9 цифр!'),
        ],
        blank=True,
        null=True,
    )
    bik = models.CharField(
        'БИК',
        max_length=9,
        validators=[
            RegexValidator(r'^[\d]{9}$', message='БИК состоит из 9 цифр!'),
        ],
        blank=True,
        null=True,
    )
    payment_account = models.CharField(
        'расчетный счет',
        max_length=20,
        validators=[
            RegexValidator(
                r'^[\d]{20}$',
                message='Расчетный счет состоит из 20 цифр!',
            ),
        ],
        blank=True,
        null=True,
    )
    correspondent_account = models.CharField(
        'корреспондентский счет',
        max_length=20,
        validators=[
            RegexValidator(
                r'^[\d]{20}$',
                message='Корреспондентский счет состоит из 20 цифр!',
            ),
        ],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'продавец'
        verbose_name_plural = 'продавцы'
        ordering = ('-created',)

    def __str__(self):
        return self.user.email
