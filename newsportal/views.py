from django.shortcuts import render
from django.views.generic import ListView
from newsportal.models import Post, Comment


class PostListView(ListView):
    model = Post
    ordering = 'rating'
    template_name = 'post.html'
    context_object_name = 'posts'


# class CommentListView(ListView):
#     model = Comment
#     ordering = 'rating'
#     template_name = 'comment.html'
#     context_object_name = 'comments'
