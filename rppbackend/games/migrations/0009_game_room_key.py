# Generated by Django 3.2.8 on 2021-12-02 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_alter_gameinvitation_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='room_key',
            field=models.TextField(default='', max_length=256),
        ),
    ]
