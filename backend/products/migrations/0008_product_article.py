from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0007_remove_product_article"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="article",
            field=models.PositiveIntegerField(
                default=0,
                verbose_name="артикул",
            ),
            preserve_default=False,
        ),
    ]
