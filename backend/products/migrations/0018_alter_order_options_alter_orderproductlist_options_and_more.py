from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0017_image_imageproduct_product_images"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={
                "ordering": ("-created",),
                "verbose_name": "заказ",
                "verbose_name_plural": "заказы",
            },
        ),
        migrations.AlterModelOptions(
            name="orderproductlist",
            options={
                "ordering": ["order"],
                "verbose_name": "товар в заказе",
                "verbose_name_plural": "товары в заказах",
            },
        ),
        migrations.AlterModelOptions(
            name="shoppingcart",
            options={
                "verbose_name": "корзина пользователя",
                "verbose_name_plural": "корзины пользователей",
            },
        ),
        migrations.AlterModelOptions(
            name="shoppingcart_items",
            options={
                "verbose_name": "товар в корзине",
                "verbose_name_plural": "товары в корзине",
            },
        ),
    ]
