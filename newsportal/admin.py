from django.contrib import admin
from .models import Author, Tag, Comment, Post, PostCategory

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(PostCategory)

