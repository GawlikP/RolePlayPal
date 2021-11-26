from django.urls import path 

from .views import ProfileDetailView, ProfileListView, ProfileDetailSlugView, ProfileUserIdView,ProfileActualUserView

urlpatterns = [
    path('', ProfileListView, name='get list and post endpoint'),
    path('<int:pk>/', ProfileDetailView, name='get detail and put endpoint'),
    path('me/', ProfileActualUserView, name='get actual user profile'),
    path('<slug:profile_slug>/', ProfileDetailSlugView, name='get detail and put endpoint by slug'),
    path('user/<int:pk>/', ProfileUserIdView, name='get detail and put by user id'),
   
]
