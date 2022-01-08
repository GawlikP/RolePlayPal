from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class PrivateMessage(models.Model):
    created = models.DateTimeField(auto_now_add=True, blank=False)
    sended = models.DateTimeField(blank=True, null=True)
    text = models.TextField(max_length=2048)
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_user')
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_user')
    readed = models.BooleanField(default=False)

    def __str__(self):
        return 'date:' + self.created.strftime('%Y-%m-%d %H:%M') + ' from:' + self.sender_user.username + ' to:' + self.receiver_user.username 

    class Meta:
        ordering = ('-created',)

status_choices = (
    ('B', 'BLOCKED'),
    ('A', 'ALLOWED'),
    ('W', 'WAITING'),
)

class MessageCredential(models.Model):
    created = models.DateTimeField(auto_now_add=True, blank=False)
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_from')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to')
    status = models.CharField(max_length=1, choices=status_choices)

    def __str__(self):
        return 'from: ' + self.user_from.username + ' to:' + self.user_to.username + ' status:' + self.status

    class Meta:
        ordering  = ('-created',)