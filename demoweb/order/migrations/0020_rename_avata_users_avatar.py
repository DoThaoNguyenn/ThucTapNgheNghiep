# Generated by Django 4.2.3 on 2023-07-28 08:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0019_users_avata"),
    ]

    operations = [
        migrations.RenameField(
            model_name="users",
            old_name="avata",
            new_name="avatar",
        ),
    ]
