# Generated by Django 4.2.3 on 2023-07-27 09:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0017_remove_district_city_remove_ward_district_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="street",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
