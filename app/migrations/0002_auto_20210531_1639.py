# Generated by Django 3.2 on 2021-05-31 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
