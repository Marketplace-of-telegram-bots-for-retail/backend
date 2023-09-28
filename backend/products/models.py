from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User


class Product(models.Model):
    ...


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
                fields=['user, product'], name='rating_allowed_once')
        ]

    def __str__(self):
        return self.text
