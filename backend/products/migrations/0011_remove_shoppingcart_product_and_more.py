import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0010_alter_review_rating"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="shoppingcart",
            name="product",
        ),
        migrations.RemoveField(
            model_name="shoppingcart",
            name="quantity",
        ),
        migrations.RemoveField(
            model_name="shoppingcart",
            name="user",
        ),
        migrations.AddField(
            model_name="shoppingcart",
            name="owner",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_cart",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец корзины",
            ),
            preserve_default=False,
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
                        default=1,
                        verbose_name="Количество товара",
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
            options={
                "verbose_name": "товары в корзине товаров",
                "verbose_name_plural": "товары в корзине товаров",
            },
        ),
        migrations.AddField(
            model_name="shoppingcart",
            name="items",
            field=models.ManyToManyField(
                through="products.ShoppingCart_Items",
                to="products.product",
            ),
        ),
    ]
