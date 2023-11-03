import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "products",
            "0018_alter_order_options_alter_orderproductlist_options_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="image_1",
        ),
        migrations.RemoveField(
            model_name="product",
            name="image_2",
        ),
        migrations.RemoveField(
            model_name="product",
            name="image_3",
        ),
        migrations.RemoveField(
            model_name="product",
            name="image_4",
        ),
        migrations.RemoveField(
            model_name="product",
            name="category",
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(
                max_length=500,
                verbose_name="описание бота",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(
                max_length=500,
                verbose_name="название бота",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(100000000),
                ],
                verbose_name="стоимость",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="products.category",
                verbose_name="категория",
            ),
        ),
    ]
