# Generated by Django 3.2.8 on 2021-12-01 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0012_auto_20211129_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='contest_current_long',
            field=models.CharField(default='01:00:00', max_length=20),
        ),
    ]
