from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0012_alter_shoppingcart_owner"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="shoppingcart",
            options={
                "verbose_name": "Корзина товаров",
                "verbose_name_plural": "Корзина товаров",
            },
        ),
        migrations.AlterModelOptions(
            name="shoppingcart_items",
            options={
                "verbose_name": "Товар в корзине",
                "verbose_name_plural": "Товары в корзине",
            },
        ),
        migrations.AddField(
            model_name="shoppingcart",
            name="promocode",
            field=models.BooleanField(default=False, verbose_name="Промокод"),
        ),
        migrations.AddField(
            model_name="shoppingcart_items",
            name="is_selected",
            field=models.BooleanField(default=True, verbose_name="Выбран"),
        ),
    ]
