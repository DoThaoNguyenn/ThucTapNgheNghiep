# Generated by Django 4.2.3 on 2023-07-25 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_order_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total',
            new_name='total_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='menthod',
        ),
        migrations.RemoveField(
            model_name='order',
            name='note',
        ),
    ]
