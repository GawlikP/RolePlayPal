# Generated by Django 3.2.8 on 2021-12-30 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0010_auto_20211229_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='wallpapers',
        ),
        migrations.CreateModel(
            name='GameHandout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now_add=True)),
                ('name', models.TextField(max_length=512, unique=True)),
                ('slug', models.SlugField(max_length=1024)),
                ('deleted', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, upload_to='games_handouts')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game', to='games.game')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
