# Generated by Django 4.2.5 on 2023-10-18 11:39

from django.db import migrations, models

import users.models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_bayer",
        ),
        migrations.AddField(
            model_name="user",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=users.models.user_directory_path,
                verbose_name="Фотография пользователя",
            ),
        ),
    ]