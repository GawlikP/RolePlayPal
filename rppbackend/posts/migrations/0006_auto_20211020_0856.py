# Generated by Django 3.2.8 on 2021-10-20 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20211020_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='minuses',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='pluses',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
