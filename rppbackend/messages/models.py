from django.db import models
from django.contrib.auth.models import User 
from django.utils.text import slugify
import string 
from profiles.models import unique_slugify
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
# Create your models here

class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sended = models.BooleanField(default=False)
    text = models.TextField()
    title = models.TextField(max_length=1024)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_user')
    receiver_user = models = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_user')
    readed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ('-created',) 

@receiver(post_save, sender=Message)
def update_slug_field(sender, instance, created, **kwags):
    if created:
        instance.slug = unique_slugify(instance, slugify(instance.name))
        instance.save()
