from django.urls import path 

from .views import ProfileDetailView, ProfileListView

urlpatterns = [
    path('', ProfileListView, name='get list and post endpoint'),
    path('<int:pk>', ProfileDetailView, name='get detail and put endpoint'),

]