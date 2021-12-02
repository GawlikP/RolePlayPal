# Generated by Django 3.2.8 on 2021-11-29 07:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now_add=True)),
                ('next_game', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('name', models.TextField(max_length=512, unique=True)),
                ('slug', models.SlugField(blank=True, default='', max_length=1024)),
                ('image', models.ImageField(blank=True, upload_to='game_wallpapers')),
                ('players', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]