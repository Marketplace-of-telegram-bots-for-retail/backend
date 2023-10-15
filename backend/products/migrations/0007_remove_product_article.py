from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_alter_product_article"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="article",
        ),
    ]
