# Generated by Django 2.2 on 2020-12-13 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_auto_20201212_2025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
    ]