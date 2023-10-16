# Generated by Django 4.2.5 on 2023-10-16 17:21

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import products.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

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
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=200, verbose_name="название")),
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
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_paid", models.BooleanField(default=False, verbose_name="оплачен")),
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
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="название бота"),
                ),
                ("description", models.TextField(verbose_name="описание бота")),
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
                (
                    "video",
                    models.TextField(
                        blank=True, null=True, verbose_name="ссылка на видео"
                    ),
                ),
                (
                    "article",
                    models.PositiveIntegerField(
                        default=products.models.Product.get_article,
                        editable=False,
                        unique=True,
                        verbose_name="артикул",
                    ),
                ),
                (
                    "price",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="стоимость",
                    ),
                ),
                (
                    "category",
                    models.ManyToManyField(
                        blank=True,
                        to="products.category",
                        verbose_name="список категорий",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
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
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "корзина товаров",
                "verbose_name_plural": "корзина товаров",
            },
        ),
        migrations.CreateModel(
            name="ShoppingCart_Items",
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
                    models.PositiveSmallIntegerField(
                        default=1, verbose_name="Количество товара"
                    ),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.shoppingcart",
                        verbose_name="Корзина",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shop_cart",
                        to="products.product",
                        verbose_name="Продукт",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="shoppingcart",
            name="items",
            field=models.ManyToManyField(
                through="products.ShoppingCart_Items", to="products.product"
            ),
        ),
        migrations.AddField(
            model_name="shoppingcart",
            name="owner",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_cart",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец корзины",
            ),
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
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
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
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_review",
                        to="products.product",
                        verbose_name="продукт",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_review",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
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
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="количество продуктов",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_in_order",
                        to="products.order",
                        verbose_name="связанные заказы",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="order_with_product",
                        to="products.product",
                        verbose_name="связанные продукты",
                    ),
                ),
            ],
            options={
                "verbose_name": "продукт",
                "verbose_name_plural": "продукты в заказах",
                "ordering": ["order"],
            },
        ),
        migrations.AddField(
            model_name="order",
            name="product_list",
            field=models.ManyToManyField(
                related_name="product_in_order",
                through="products.OrderProductList",
                to="products.product",
                verbose_name="продукт в заказе",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_orders",
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.CreateModel(
            name="Favorite",
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
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_favorite",
                        to="products.product",
                        verbose_name="продукт",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_favorite",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "избранное",
                "verbose_name_plural": "избранные",
            },
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                fields=("user", "product"), name="rating_allowed_once"
            ),
        ),
        migrations.AddConstraint(
            model_name="orderproductlist",
            constraint=models.UniqueConstraint(
                fields=("order", "product"), name="unique_order"
            ),
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(
                fields=("user", "product"), name="unique favorite"
            ),
        ),
    ]
