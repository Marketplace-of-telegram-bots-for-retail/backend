import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import TimestampedModel
from users.models import User


def user_directory_path(instance, filename):
    return f'products/{instance.user.id}/{filename}'


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
        verbose_name='пользователь',
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
    video = models.TextField(
        'ссылка на видео',
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


class Review(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_review',
        verbose_name='пользователь',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_review',
        verbose_name='продукт',
    )
    rating = models.PositiveSmallIntegerField(
        'рейтинг',
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField(
        'текст отзыва',
        max_length=500,
        blank=True,
    )
    is_favorite = models.BooleanField(
        'избранное',
        default=False,
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('-created',)
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'user',
                    'product',
                ),
                name='rating_allowed_once',
            ),
        ]

    def __str__(self):
        return self.text


class Order(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_orders',
        verbose_name='пользователь',
    )
    product_list = models.ManyToManyField(
        Product,
        through='OrderProductList',
        related_name='product_in_order',
        verbose_name='продукт в заказе',
    )
    is_paid = models.BooleanField('оплачен', default=False)
    sale_status = models.BooleanField('скидка', default=False)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ от пользователя: {self.user}'


class OrderProductList(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='product_in_order',
        verbose_name='связанные заказы',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name='order_with_product',
        verbose_name='связанные продукты',
        null=True,
    )
    quantity = models.IntegerField(
        'количество продуктов',
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты в заказах'
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'order',
                    'product',
                ),
                name='unique_order',
            ),
        ]

    def __str__(self):
        return f'{self.product} {self.quantity} в заказе {self.order}'


class ShoppingCart(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='продукт',
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='количество товара',
    )

    def __str__(self):
        return f'Корзина пользователя {self.user}'

    class Meta:
        verbose_name = 'корзина товаров'
        verbose_name_plural = verbose_name
