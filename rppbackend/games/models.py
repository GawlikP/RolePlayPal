from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)
    next_game = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=False)
    name = models.TextField(unique=True, max_length=512)
    slug = models.SlugField(max_length=1024, blank=True, default='')
    players = models.ManyToMany(User)
    image = models.ImageField(upload_to='game_wallpapers', blank=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ('-created',)

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + get_random_string(length=4)
    return unique_slug

@receiver(post_save, sender=Game)
def update_slug_field(sender, instance, created, **kwags):
    if created:
        instance.slug = unique_slugify(instance, slugify(instance.user.username))
        instance.save()
