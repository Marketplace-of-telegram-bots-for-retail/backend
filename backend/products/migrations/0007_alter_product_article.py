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
                blank=True,
                default=products.models.Product.get_article,
                null=True,
                verbose_name="артикул",
            ),
        ),
    ]
