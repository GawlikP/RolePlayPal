from django.db import models

from posts.models import Post
from django.contrib.auth.models import User
# Create your models here.

from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

class PostReaction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.post.title + ":" + self.user.username

    class Meta:
        ordering = ['created']

@receiver(post_save, sender=PostReaction)
def update_pluses_minuses_field(sender,instance,created, **kawgs):
    if created or not created:
  
        if instance.state == True:
            instance.post.pluses += 1 
        else:
            instance.post.minuses += 1 
        instance.post.save()

@receiver(pre_delete, sender=PostReaction)
def update_pluses_minuses_before_delete(sender, instance, using, **kawgs):    
   
    if instance.state == True:
        if instance.post.pluses > 0: 
            instance.post.pluses -= 1
    else:
        if instance.post.minuses > 0:
            instance.post.minuses -= 1 
    instance.post.save()