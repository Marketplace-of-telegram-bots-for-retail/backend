from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0013_alter_shoppingcart_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="shoppingcart",
            options={"verbose_name": "Корзина товаров"},
        ),
        migrations.RemoveField(
            model_name="shoppingcart",
            name="promocode",
        ),
        migrations.AddField(
            model_name="shoppingcart",
            name="discount",
            field=models.PositiveSmallIntegerField(
                null=True,
                verbose_name="Процент скидки",
            ),
        ),
    ]
