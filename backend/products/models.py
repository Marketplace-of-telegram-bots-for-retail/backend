import uuid

from django.db import models

from core.models import TimestampedModel
from core.utils import user_directory_path
from users.models import User


class Category(TimestampedModel):
    name = models.CharField(
        'название',
        max_length=200,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> str:
        return self.name


class Product(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='продавец',
    )
    name = models.CharField(
        'название бота',
        max_length=200,
    )
    description = models.TextField(
        'описание бота',
    )
    image_1 = models.ImageField(
        'картинка №1',
        upload_to=user_directory_path,
        blank=True,
        null=True,
    )
    image_2 = models.ImageField(
        'картинка №2',
        upload_to=user_directory_path,
        blank=True,
        null=True,
    )
    image_3 = models.ImageField(
        'картинка №3',
        upload_to=user_directory_path,
        blank=True,
        null=True,
    )
    image_4 = models.ImageField(
        'картинка №4',
        upload_to=user_directory_path,
        blank=True,
        null=True,
    )
    article = models.UUIDField(
        'артикул',
        default=uuid.uuid4,
        editable=False,
    )
    price = models.IntegerField('стоимость')
    category = models.ManyToManyField(
        Category,
        verbose_name='список категорий',
        blank=True,
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.name
