import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "products",
            "0024_merge_0023_alter_product_name_0023_alter_review_text",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(
                max_length=1500,
                validators=[django.core.validators.MinLengthValidator(50)],
                verbose_name="описание бота",
            ),
        ),
    ]
