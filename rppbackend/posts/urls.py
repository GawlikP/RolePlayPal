from django.urls import path

from .views import PostListView, PostDetailView, CategoriesListView

urlpatterns = [
      path('<slug:category_slug>/<slug:post_slug>/', PostDetailView, name='post_detail'), # updated
      path('', PostListView, name='post_list'),
      path('categories/', CategoriesListView, name='categories_list')
]