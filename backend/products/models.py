from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Product(models.Model):
    pass


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
