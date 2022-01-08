from django.contrib import admin

from .models import Profile, ProfilePasswordReset
# Register your models here.

admin.site.register(Profile)
admin.site.register(ProfilePasswordReset)