# Generated by Django 4.2.5 on 2023-11-03 11:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0019_remove_product_image_1_remove_product_image_2_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(max_length=500, verbose_name="описание бота"),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=500, verbose_name="название бота"),
        ),
    ]
