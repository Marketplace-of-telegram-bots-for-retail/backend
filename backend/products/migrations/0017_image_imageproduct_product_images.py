import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import products.models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0016_alter_order_number_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=products.models.user_directory_path,
                        verbose_name="изображение",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "изображение",
                "verbose_name_plural": "изображения",
            },
        ),
        migrations.CreateModel(
            name="ImageProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.image",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "изображение в товаре",
                "verbose_name_plural": "изображения в товарах",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="images",
            field=models.ManyToManyField(
                blank=True,
                through="products.ImageProduct",
                to="products.image",
                verbose_name="список изображений",
            ),
        ),
    ]
