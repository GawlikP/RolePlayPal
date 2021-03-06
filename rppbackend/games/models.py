from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import string
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from profiles.models import unique_slugify
import string
from django.utils.crypto import get_random_string
# Create your models here.
class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)
    next_game = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=False)
    name = models.TextField(unique=True, max_length=512)
    slug = models.SlugField(max_length=1024, blank=True, default='')
    players = models.ManyToManyField(User, blank=True)
    main_wallpaper = models.ImageField(upload_to='game_wallpapers', blank=True)
    game_master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_master')
    deleted = models.BooleanField(default=False)
    room_key = models.TextField(max_length=256, default='', unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ('-created',)

    def get_main_wallpaper(self):
        if self.main_wallpaper:
            return 'http://127.0.0.1:8000' + self.main_wallpaper.url
        return ''



class GameHandout(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)
    name = models.TextField(max_length=512,blank=False, unique=True)
    slug = models.SlugField(max_length=1024)
    deleted = models.BooleanField(default=False)
    image = models.ImageField(upload_to='games_handouts', blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game')

    def __str__(self):
        return self.slug 
    
    class Meta:
        ordering = ('-created',)
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url 
        return ''

@receiver(post_save, sender=Game)
def update_slug_field(sender, instance, created, **kwags):
    if created:
        instance.slug = unique_slugify(instance, slugify(instance.name))
        
        model = instance.__class__
        room_key = get_random_string(length=250)
        while model.objects.filter(room_key=room_key).exists():
            room_key = get_random_string(length=250)
        instance.room_key = room_key
        instance.save()

@receiver(post_save, sender=GameHandout)
def update_slug_field(sender, instance, created, **kwags):
    if created:
        instance.slug = unique_slugify(instance, slugify(instance.name))
        instance.save()

class GameInvitation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)
    game_master_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_master_sender')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player')
    text = models.TextField(blank=False, default='Zaprasza ci?? do swojej rozgrywki')
    readed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    hide = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.game_master_sender.username + " Game: " + self.game.slug + " receiver:" + self.player.username

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return "/"+ self.game.slug + "/invitations/" + str(self.pk) 
