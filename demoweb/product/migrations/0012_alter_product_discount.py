# Generated by Django 4.2.3 on 2023-08-08 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_remove_review_rating_star_json'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
