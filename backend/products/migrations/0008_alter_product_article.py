from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0007_alter_product_article"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="article",
            field=models.PositiveIntegerField(
                unique=True,
                verbose_name="артикул",
            ),
        ),
    ]
