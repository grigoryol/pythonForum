# Generated by Django 3.2 on 2021-06-22 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210615_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='static/img/ava.jpg', upload_to='static/upload/', verbose_name='avatar'),
        ),
    ]
