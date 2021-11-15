from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    note = models.TextField(max_length=512)
    preffered_role = models.BooleanField(defualt=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.account.username + " " + self.note

    class Meta: 
        ordering =(-'created')
