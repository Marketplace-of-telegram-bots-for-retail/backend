from django.db import migrations, models

import products.models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0008_product_article"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="article",
            field=models.PositiveIntegerField(
                default=products.models.Product.get_article,
                editable=False,
                unique=True,
                verbose_name="артикул",
            ),
        ),
    ]
