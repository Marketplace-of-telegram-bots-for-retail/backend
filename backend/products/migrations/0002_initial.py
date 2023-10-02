import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="shoppingcart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_review",
                to="products.product",
                verbose_name="продукт",
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_review",
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ManyToManyField(
                blank=True,
                to="products.category",
                verbose_name="список категорий",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="orderproductlist",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_in_order",
                to="products.order",
                verbose_name="связанные заказы",
            ),
        ),
        migrations.AddField(
            model_name="orderproductlist",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="order_with_product",
                to="products.product",
                verbose_name="связанные продукты",
            ),
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
    ]
