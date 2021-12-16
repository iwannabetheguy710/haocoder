# Generated by Django 3.2.8 on 2021-12-16 11:50

from django.db import migrations, models
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_profile_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField(default='', max_length=1000)),
                ('content', martor.models.MartorField(default='')),
                ('visible', models.BooleanField(default=True)),
            ],
        ),
    ]