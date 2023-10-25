import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0014_alter_shoppingcart_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={
                "ordering": ("-created",),
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
            },
        ),
        migrations.AlterModelOptions(
            name="orderproductlist",
            options={
                "ordering": ["order"],
                "verbose_name": "Продукт",
                "verbose_name_plural": "Продукты в заказах",
            },
        ),
        migrations.AddField(
            model_name="order",
            name="number_order",
            field=models.PositiveIntegerField(
                default=0, editable=False, verbose_name="Номер заказа",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="pay_method",
            field=models.CharField(
                blank=True,
                choices=[("card", "card"), ("sbp", "sbp")],
                max_length=4,
                null=True,
                verbose_name="Метод оплаты",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="send_to",
            field=models.EmailField(
                blank=True, max_length=200, verbose_name="Куда прислать",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="is_paid",
            field=models.BooleanField(default=False, verbose_name="Оплачен"),
        ),
        migrations.AlterField(
            model_name="order",
            name="sale_status",
            field=models.BooleanField(default=False, verbose_name="Скидка"),
        ),
        migrations.AlterField(
            model_name="orderproductlist",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_in_order",
                to="products.order",
                verbose_name="Связанные заказы",
            ),
        ),
        migrations.AlterField(
            model_name="orderproductlist",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="order_with_product",
                to="products.product",
                verbose_name="Связанные продукты",
            ),
        ),
        migrations.AlterField(
            model_name="orderproductlist",
            name="quantity",
            field=models.IntegerField(
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Количество продуктов",
            ),
        ),
    ]
