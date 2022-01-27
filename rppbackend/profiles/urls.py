from django.urls import path 

from .views import ProfileDetailView, ProfileListView, ProfileDetailSlugView, ProfileUserIdView,ProfileActualUserView, ProfilePlayersList
from .views import ProfileMastersList, UserResetProfilePassword, UserResetProfilePasswordByEmail, UserSetPasswordView
urlpatterns = [
    path('', ProfileListView, name='get list and post endpoint'),
    path('<int:pk>/', ProfileDetailView, name='get detail and put endpoint'),
    path('me/', ProfileActualUserView, name='get actual user profile'),
    path('<slug:profile_slug>/', ProfileDetailSlugView, name='get detail and put endpoint by slug'),
    path('<slug:profile_slug>/players/', ProfilePlayersList, name='get all players of that profile'),
    path('<slug:profile_slug>/masters/', ProfileMastersList, name='get all masters of that profile'),
    path('user/<int:pk>/', ProfileUserIdView, name='get detail and put by user id'),
    path('me/reset_password/', UserResetProfilePassword, name='post password reset request'),
    #path('me/reset_password/email/<str:user_email>/', UserResetProfilePasswordByEmail, name='post reset password of email'),
    #path('me/set_password/', UserSetPasswordView, name='post for reseting password on actual requesting user, needed old_password and new_password'),

   
]
