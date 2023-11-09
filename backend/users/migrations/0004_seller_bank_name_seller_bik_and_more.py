import django.core.validators
from django.db import migrations, models

import users.models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_seller"),
    ]

    operations = [
        migrations.AddField(
            model_name="seller",
            name="bank_name",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Сбербанк", "Сбербанк"),
                    ("Тинькофф", "Тинькофф"),
                    ("Альфа-Банк", "Альфа-Банк"),
                    ("ВТБ Банк", "ВТБ Банк"),
                    ("Газпромбанк", "Газпромбанк"),
                    ("Райффайзен Банк", "Райффайзен Банк"),
                ],
                max_length=15,
                null=True,
                verbose_name="название банка",
            ),
        ),
        migrations.AddField(
            model_name="seller",
            name="bik",
            field=models.CharField(
                blank=True,
                max_length=9,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[\\d]{9}$",
                        message="БИК состоит из 9 цифр!",
                    ),
                ],
                verbose_name="БИК",
            ),
        ),
        migrations.AddField(
            model_name="seller",
            name="correspondent_account",
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[\\d]{20}$",
                        message="Корреспондентский счет состоит из 20 цифр!",
                    ),
                ],
                verbose_name="корреспондентский счет",
            ),
        ),
        migrations.AddField(
            model_name="seller",
            name="kpp",
            field=models.CharField(
                blank=True,
                max_length=9,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[\\d]{9}$",
                        message="КПП состоит из 9 цифр!",
                    ),
                ],
                verbose_name="КПП",
            ),
        ),
        migrations.AddField(
            model_name="seller",
            name="logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=users.models.seller_directory_path,
                verbose_name="логотип магазина",
            ),
        ),
        migrations.AddField(
            model_name="seller",
            name="ogrn",
            field=models.CharField(
                blank=True,
                max_length=15,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[\\d]{13}$|^[\\d]{15}$",
                        message="ОГРН состоит из 13 цифр для юридического лица или 15 цифр для ИП!",
                    ),
                ],
                verbose_name="ОГРН",
            ),
        ),
        migrations.AddField(
            model_name="seller",
            name="organization_name",
            field=models.TextField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="название организации",
            ),
        ),
        migrations.AddField(
            model_name="seller",
            name="organization_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ООО", "ООО"),
                    ("ОДО", "ОДО"),
                    ("ОА", "ОА"),
                    ("АО", "АО"),
                    ("ПАО", "ПАО"),
                    ("ПТ", "ПТ"),
                    ("ТНВ", "ТНВ"),
                    ("ПК", "ПК"),
                    ("ИП", "ИП"),
                    ("ОАО", "ОАО"),
                    ("Самозанятый", "Самозанятый"),
                ],
                max_length=11,
                null=True,
                verbose_name="тип организации",
            ),
        ),
        migrations.AddField(
            model_name="seller",
            name="payment_account",
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[\\d]{20}$",
                        message="Расчетный счет состоит из 20 цифр!",
                    ),
                ],
                verbose_name="расчетный счет",
            ),
        ),
        migrations.AddField(
            model_name="seller",
            name="store_name",
            field=models.TextField(
                blank=True,
                max_length=25,
                null=True,
                verbose_name="название магазина",
            ),
        ),
        migrations.AlterField(
            model_name="seller",
            name="inn",
            field=models.CharField(
                max_length=12,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[\\d]{10}$|^[\\d]{12}$",
                        message="ИНН состоит из 10 цифр для юридического лица или 12 цифр для физического лица!",
                    ),
                ],
                verbose_name="ИНН",
            ),
        ),
    ]
