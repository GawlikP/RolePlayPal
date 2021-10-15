from django.urls import path

from .views import PostListView, PostDetailView, CategoriesListView, PostReactionsListView, UserPostReactionsView, PostsReactionsListView, UserPostsReactionsView

urlpatterns = [
      path('reactions/', PostsReactionsListView, name='posts_reactions'),
      path('reactions/me/', UserPostsReactionsView, name='user_reactions_list'),
      path('<slug:category_slug>/<slug:post_slug>/', PostDetailView, name='post_detail'), # updated
      path('', PostListView, name='post_list'),
      path('categories/', CategoriesListView, name='categories_list'),
      path('<slug:category_slug>/<slug:post_slug>/reactions/', PostReactionsListView, name='reactions_list'),
      path('<slug:category_slug>/<slug:post_slug>/reactions/me/', UserPostReactionsView, name='user_post_reactions_list'),
      

]