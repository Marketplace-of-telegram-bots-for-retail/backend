import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_remove_review_is_favorite_favorite_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.PositiveIntegerField(
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="стоимость",
            ),
        ),
    ]
