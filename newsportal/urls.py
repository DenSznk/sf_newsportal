from django.urls import path
from .views import PostListView, PostDetails

urlpatterns = [
    path('', PostListView.as_view()),
    path('<int:pk>', PostDetails.as_view()),
]