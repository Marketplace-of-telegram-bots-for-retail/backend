import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0021_order_total_cost"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="text",
            field=models.TextField(
                blank=True,
                max_length=500,
                validators=[django.core.validators.MinLengthValidator(6)],
                verbose_name="текст отзыва",
            ),
        ),
    ]
