# Generated by Django 4.2.5 on 2023-10-15 07:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0007_alter_product_article"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="article",
            field=models.PositiveIntegerField(unique=True, verbose_name="артикул"),
        ),
    ]
