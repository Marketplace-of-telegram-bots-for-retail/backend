import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_remove_user_is_bayer_user_photo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Seller",
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
                    "inn",
                    models.CharField(
                        max_length=12,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[\\d+]{10,12}$",
                            ),
                        ],
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "продавец",
                "verbose_name_plural": "продавцы",
                "ordering": ("-created",),
            },
        ),
    ]
