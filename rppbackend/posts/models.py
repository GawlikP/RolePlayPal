
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

from post_category.models import PostCategory

from django.core.validators import MinValueValidator

def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + get_random_string(length=4)
    return unique_slug


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True, blank=True)
    deleted = models.BooleanField(default=False)
    title = models.CharField(max_length=1024,blank=False)
    content = models.TextField(default='')
    tags = models.TextField(blank=True, default='')
    pluses = models.PositiveIntegerField(default=0)
    minuses = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    shadowed = models.BooleanField(default=False)
    reports = models.IntegerField(default=0)
    category = models.ForeignKey(PostCategory, related_name='post_category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    slug = models.SlugField(max_length=1024,default="",blank=True, null=True)
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ('-created',) 

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            self.slug = unique_slugify(self, slug)
        super(Post, self).save(*args, **kwargs)

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
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

