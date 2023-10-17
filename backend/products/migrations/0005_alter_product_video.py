from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0004_alter_product_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="video",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="ссылка на видео",
            ),
        ),
    ]
