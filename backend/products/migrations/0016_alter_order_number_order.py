from django.db import migrations, models

import products.models


class Migration(migrations.Migration):
    dependencies = [
        (
            "products",
            "0015_alter_order_options_alter_orderproductlist_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="number_order",
            field=models.PositiveIntegerField(
                default=products.models.Order.get_number_order,
                editable=False,
                unique=True,
                verbose_name="Номер заказа",
            ),
        ),
    ]
