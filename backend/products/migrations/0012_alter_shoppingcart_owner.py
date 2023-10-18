import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0011_remove_shoppingcart_product_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shoppingcart",
            name="owner",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_cart",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец корзины",
            ),
        ),
    ]
