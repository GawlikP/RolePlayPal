from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    note = models.TextField(max_length=512)
    preffered_role = models.BooleanField(default=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " " + self.note

    class Meta: 
        ordering = ('-created',) 
