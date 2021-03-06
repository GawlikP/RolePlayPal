# Generated by Django 3.2.8 on 2021-10-15 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20211013_1239'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created',)},
        ),
        migrations.RemoveField(
            model_name='post',
            name='date_added',
        ),
        migrations.AlterField(
            model_name='post',
            name='deleted',
            field=models.BooleanField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
