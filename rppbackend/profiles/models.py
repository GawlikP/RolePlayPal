
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify
import string
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
# Create your models here.

def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + get_random_string(length=4)
    return unique_slug


class Profile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    note = models.TextField(max_length=512)
    preferred_role = models.BooleanField(default=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    slug = models.SlugField(max_length=1024,blank=True, default='')
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.slug

    class Meta: 
        ordering = ('-created',) 
    
    

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return '' 

    def make_thumbnail(self, image, size=(800,640)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

@receiver(post_save, sender=Profile)
def update_pluses_minuses_field(sender,instance,created, **kawgs):
    if created:
        instance.slug  = unique_slugify(instance, slugify(instance.user.username))
        
        instance.save()

