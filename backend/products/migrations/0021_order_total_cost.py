from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "products",
            "0020_alter_product_category_alter_product_description_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="total_cost",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Итоговая цена",
            ),
        ),
    ]
