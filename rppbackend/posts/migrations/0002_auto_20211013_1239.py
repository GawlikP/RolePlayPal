# Generated by Django 3.2.8 on 2021-10-13 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.TextField(blank=True, default=''),
        ),
    ]
