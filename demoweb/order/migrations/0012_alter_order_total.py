# Generated by Django 4.2.3 on 2023-07-19 03:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0011_alter_users_options_users_address_users_phone_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="total",
            field=models.FloatField(default=0),
        ),
    ]
