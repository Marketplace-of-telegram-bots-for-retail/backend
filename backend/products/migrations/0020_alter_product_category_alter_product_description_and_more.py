import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "products",
            "0019_remove_product_image_1_remove_product_image_2_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="products.category",
                verbose_name="категория",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(
                max_length=500,
                validators=[django.core.validators.MinLengthValidator(50)],
                verbose_name="описание бота",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(
                max_length=70,
                validators=[django.core.validators.MinLengthValidator(20)],
                verbose_name="название бота",
            ),
        ),
    ]
