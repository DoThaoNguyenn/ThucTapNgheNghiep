# Generated by Django 4.2.2 on 2023-08-13 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0030_alter_users_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='question',
            field=models.CharField(choices=[(1, 'Cuốn sách yêu thích nhất của bạn?'), (2, 'Cuốn sách đầu tiên bạn đọc?'), (3, 'Loài động vật bản yêu thích nhất?')], default='1', max_length=255),
        ),
    ]
