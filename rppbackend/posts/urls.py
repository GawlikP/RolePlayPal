from django.urls import path

from .views import PostListView, PostDetailView, CategoriesListView, PostReactionsListView, UserPostReactionsView, PostsReactionsListView, UserPostsReactionsView
from .views import PostCommentListView, PostCommentDetailView, PostCategoryListView, testView



urlpatterns = [
      path('test/', testView, name='test'),
      path('comments/<int:pk>/', PostCommentDetailView, name='postcomment_detail'),
      path('reactions/', PostsReactionsListView, name='posts_reactions'),
      path('reactions/me/', UserPostsReactionsView, name='user_reactions_list'),
      path('<slug:category_slug>/<slug:post_slug>/', PostDetailView, name='post_detail'), # updated
      path('', PostListView, name='post_list'),
      path('categories/', CategoriesListView, name='categories_list'),
      path('<slug:category_slug>/<slug:post_slug>/reactions/', PostReactionsListView, name='reactions_list'),
      path('<slug:category_slug>/<slug:post_slug>/reactions/me/', UserPostReactionsView, name='user_post_reactions_list'),
      path('<slug:category_slug>/<slug:post_slug>/comments/', PostCommentListView, name='postcomment_list_and_post'),
      path('<slug:category_slug>/', PostCategoryListView, name='all post in category'),
      
  
]