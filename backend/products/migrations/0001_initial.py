import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import products.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="название"),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "is_paid",
                    models.BooleanField(default=False, verbose_name="оплачен"),
                ),
                (
                    "sale_status",
                    models.BooleanField(default=False, verbose_name="скидка"),
                ),
            ],
            options={
                "verbose_name": "заказ",
                "verbose_name_plural": "заказы",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="OrderProductList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                        verbose_name="количество продуктов",
                    ),
                ),
            ],
            options={
                "verbose_name": "продукт",
                "verbose_name_plural": "продукты в заказах",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "name",
                    models.CharField(
                        max_length=200, verbose_name="название бота"
                    ),
                ),
                (
                    "description",
                    models.TextField(verbose_name="описание бота"),
                ),
                (
                    "image_1",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=products.models.user_directory_path,
                        verbose_name="картинка №1",
                    ),
                ),
                (
                    "image_2",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=products.models.user_directory_path,
                        verbose_name="картинка №2",
                    ),
                ),
                (
                    "image_3",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=products.models.user_directory_path,
                        verbose_name="картинка №3",
                    ),
                ),
                (
                    "image_4",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=products.models.user_directory_path,
                        verbose_name="картинка №4",
                    ),
                ),
                ("video", models.TextField(verbose_name="ссылка на видео")),
                (
                    "article",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        verbose_name="артикул",
                    ),
                ),
                ("price", models.IntegerField(verbose_name="стоимость")),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                        verbose_name="рейтинг",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        blank=True, max_length=500, verbose_name="текст отзыва"
                    ),
                ),
                (
                    "is_favorite",
                    models.BooleanField(
                        default=False, verbose_name="избранное"
                    ),
                ),
            ],
            options={
                "verbose_name": "отзыв",
                "verbose_name_plural": "отзывы",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="ShoppingCart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "quantity",
                    models.PositiveSmallIntegerField(
                        default=1, verbose_name="количество товара"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                        verbose_name="продукт",
                    ),
                ),
            ],
            options={
                "verbose_name": "корзина товаров",
                "verbose_name_plural": "корзина товаров",
            },
        ),
    ]
