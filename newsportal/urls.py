from django.urls import path
from .views import PostListView, PostDetails, \
    PostUpdate, PostDelete, CreatePost, PostSearch

urlpatterns = [
    path('', PostListView.as_view()),
    path('<int:pk>', PostDetails.as_view()),
    path('news/search', PostSearch.as_view(), name='post_list'),


    path('create/news/', CreatePost.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('create/article/', CreatePost.as_view(), name='post_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

]
