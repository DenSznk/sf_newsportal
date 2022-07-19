from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from newsportal.models import Post, Comment


class PostListView(ListView):
    model = Post
    ordering = '-rating'
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['New posts is coming soon'] = None
        return context


class PostDetails(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['New posts is coming soon'] = None
        return context

# class CommentListView(ListView):
#     model = Comment
#     ordering = 'rating'
#     template_name = 'comment.html'
#     context_object_name = 'comments'
