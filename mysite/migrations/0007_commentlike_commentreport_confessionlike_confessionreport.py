# Generated by Django 2.2 on 2020-12-13 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_auto_20201213_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfessionReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('confession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.Confession')),
            ],
        ),
        migrations.CreateModel(
            name='ConfessionLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positive', models.BooleanField()),
                ('confession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.Confession')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.User')),
            ],
        ),
        migrations.CreateModel(
            name='CommentReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positive', models.BooleanField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.User')),
            ],
        ),
    ]