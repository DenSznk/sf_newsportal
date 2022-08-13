from allauth.account.views import LoginView, LogoutView
from django.urls import path
from .views import PostListView, PostDetails, \
    PostUpdate, PostDelete, CreatePost, PostSearch, upgrade_me

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('<int:pk>', PostDetails.as_view(), name='post_detail'),
    path('news/search', PostSearch.as_view(), name='post_list'),

    path('create/news/', CreatePost.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('create/article/', CreatePost.as_view(), name='post_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
]
