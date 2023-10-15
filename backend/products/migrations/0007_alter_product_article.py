from django.db import migrations, models

import products.models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_alter_product_article"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="article",
            field=models.PositiveIntegerField(
                default=products.models.Product.get_article,
                unique=True,
                verbose_name="артикул",
            ),
        ),
    ]
