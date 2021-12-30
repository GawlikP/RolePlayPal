from django.contrib import admin

# Register your models here.

from .models import Game, GameInvitation, GameHandout
# Register your models here.


admin.site.register(Game)
admin.site.register(GameInvitation)
admin.site.register(GameHandout)