from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_seller_bank_name_seller_bik_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=30),
        ),
    ]
