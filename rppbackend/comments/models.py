from django.db import models
from django.db.models.base import ModelState
from posts.models import Post
from django.contrib.auth.models import User



class PostComment(models.Model):
    created = models.DateTimeField(auto_now_add= True)
    shadowed = models.BooleanField(default= False)
    baned = models.BooleanField(default= False)
    deleted = models.BooleanField(default= False)
    content = models.TextField(null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user.username + ":" + self.post.title + ":" + str(self.pk)
    
    class Meta:
        ordering = ('-created',)
    