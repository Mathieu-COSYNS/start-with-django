# Generated by Django 2.2 on 2020-12-11 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=128)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('X', 'X')], max_length=1)),
            ],
        ),
    ]
