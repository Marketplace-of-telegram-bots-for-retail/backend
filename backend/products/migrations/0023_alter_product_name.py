import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0022_alter_review_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(
                max_length=60,
                validators=[django.core.validators.MinLengthValidator(20)],
                verbose_name="название бота",
            ),
        ),
    ]
