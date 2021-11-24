from django.urls import path 

from .views import ProfileDetailView, ProfileListView, ProfileDetailSlugView

urlpatterns = [
    path('', ProfileListView, name='get list and post endpoint'),
    path('<int:pk>/', ProfileDetailView, name='get detail and put endpoint'),
    path('<slug:profile_slug>/', ProfileDetailSlugView, name='get detail and put endpoint by slug'),
]
