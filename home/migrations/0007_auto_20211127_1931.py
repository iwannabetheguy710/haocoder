# Generated by Django 3.2.8 on 2021-11-27 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_profile_highest_ratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='highest_color',
            field=models.CharField(default='gray', max_length=7),
        ),
        migrations.AddField(
            model_name='profile',
            name='highest_role',
            field=models.CharField(default='Class H', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(default='Class H', max_length=100),
        ),
    ]
