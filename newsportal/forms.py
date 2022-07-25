from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'category',
            'header_news',
            'post_text',
            'author',
        ]


class DateInput(forms.DateField):
    input_type = 'date'


class SearchForm(forms.Form):
    date_field = forms.DateField()
