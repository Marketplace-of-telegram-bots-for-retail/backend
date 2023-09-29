from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User


class Product(models.Model):
    ...
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
