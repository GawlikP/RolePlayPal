from django.contrib import admin

# Register your models here.

from .models import Game, GameInvitation
# Register your models here.


admin.site.register(Game)
admin.site.register(GameInvitation)