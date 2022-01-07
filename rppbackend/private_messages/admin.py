from django.contrib import admin
from .models import PrivateMessage, MessageCredential

admin.site.register(PrivateMessage)
admin.site.register(MessageCredential)