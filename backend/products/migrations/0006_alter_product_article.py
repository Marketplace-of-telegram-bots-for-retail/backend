from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0005_alter_product_video"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="article",
            field=models.UUIDField(
                blank=True,
                null=True,
                verbose_name="артикул",
            ),
        ),
    ]
