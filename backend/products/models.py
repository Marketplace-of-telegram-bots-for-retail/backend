import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User
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
    pass


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_review',
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_review',
        verbose_name='Продукт'
    )
    rating = models.PositiveSmallIntegerField(
        max_length=5,
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True,
        verbose_name='Рейтинг'
    )
    text = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Текст отзыва'
    )
    is_favorite = models.BooleanField(
        default=False,
        verbose_name='Избранное'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            UniqueConstraint(
                fields=['user, product'],
                name='rating_allowed_once'
            )
        ]

    def __str__(self):
        return self.text


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_orders',
        verbose_name='Пользователь',
    )
    product_list = models.ManyToManyField(
        Product,
        through='Order_product_list',
        related_name='product_in_order',
        verbose_name='Продукт в заказе',
    )
    is_paid = models.BooleanField(default=False, verbose_name='Оплачен')
    sale_status = models.BooleanField(default=False, verbose_name='Скидка')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата редактирования'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = ('Заказ')
        verbose_name_plural = ('Заказы')

    def __str__(self):
        return f'order by {self.user}'


class Order_product_list(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='product_in_order',
        verbose_name='Связанные заказы',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name='order_with_product',
        verbose_name='Связанные продукты',
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество продуктов',
    )

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=('order', 'product', ),
                name='unique_order'),
        ]
        verbose_name = ('Продукт')
        verbose_name_plural = ('Продукты в заказах')

    def __str__(self):
        return f'{self.product} {self.quantity} in {self.order}'
