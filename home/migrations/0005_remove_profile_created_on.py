# Generated by Django 3.2.8 on 2021-11-27 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_profile_created_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='created_on',
        ),
    ]