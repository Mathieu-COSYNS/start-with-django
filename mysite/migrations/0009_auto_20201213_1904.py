# Generated by Django 2.2 on 2020-12-13 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0008_auto_20201213_1732'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hashtag',
            options={'ordering': ['name']},
        ),
    ]