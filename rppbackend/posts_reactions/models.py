from django.db import models

from posts.models import Post
from django.contrib.auth.models import User
# Create your models here.


class PostReaction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.post.title + ":" + self.user.username

    class Meta:
        ordering = ['created']

