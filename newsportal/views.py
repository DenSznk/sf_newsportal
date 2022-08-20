from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
    TemplateView,
)

from newsportal.filters import PostFilter
from newsportal.forms import PostForm, EditForm
from newsportal.models import Post, Author


def index(request):
    return HttpResponse('<h1> main Page </h1>')


class PostSearch(ListView):
    model = Post
    ordering = '-rating'
    template_name = 'search_post.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostListView(ListView):
    model = Post
    ordering = '-rating'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3


class PostDetails(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['New posts is coming soon'] = None
        return context


def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/posts/')
    return render(request, 'post_edit.html', {'form': form})


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = EditForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author_id = self.request.user.author.id
        obj.save()
        return super().form_valid(form)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'newsportal/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/')
