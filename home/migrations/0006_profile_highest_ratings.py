# Generated by Django 3.2.8 on 2021-11-27 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_profile_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='highest_ratings',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
