# Generated by Django 4.2.3 on 2023-08-04 09:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0010_review_rating_star_json"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="rating_star_json",
        ),
    ]
