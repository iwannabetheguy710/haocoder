# Generated by Django 3.2.8 on 2021-11-27 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='color',
            field=models.CharField(default='gray', max_length=7),
        ),
    ]
