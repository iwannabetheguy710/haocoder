# Generated by Django 3.2.8 on 2021-11-28 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0008_auto_20211128_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaderboard',
            name='scoring',
            field=models.CharField(blank=True, default='0', max_length=300),
        ),
    ]
