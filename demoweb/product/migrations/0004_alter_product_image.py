# Generated by Django 4.2.3 on 2023-07-13 03:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0003_alter_product_cost_alter_product_discount_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(upload_to="media"),
        ),
    ]
