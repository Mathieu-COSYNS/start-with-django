# Generated by Django 2.2 on 2020-12-13 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0005_auto_20201213_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confession',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='mysite.Hashtag'),
        ),
    ]
