# Generated by Django 4.2.3 on 2023-08-04 09:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0009_alter_review_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="rating_star_json",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
