# Generated by Django 3.2.8 on 2021-11-28 08:41

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0006_contest_contest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='contest_description',
            field=martor.models.MartorField(default=''),
        ),
    ]
