from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group

from .models import Post, Author, Comment


class PostForm(forms.ModelForm):
    '''Форма создания поста'''

    class Meta:
        model = Post
        fields = [
            'category',
            'header_news',
            'post_text',
        ]
        widgets = {
            'header_news': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Header'}),
            'post_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Input Post'}),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'category',
            'header_news',
            'post_text',
        ]
        widgets = {
            'header_news': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Header'}),
            'post_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Input Post'}),
        }


class DateInput(forms.DateField):
    input_type = 'date'


class SearchForm(forms.Form):
    date_field = forms.DateField()


class BasicSignupForm(SignupForm):
    '''Add user to common group'''

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = [
#             'comment_text',
#             'comment_date',
#             'rating',
#         ]
#         widgets = {
#             'comment_text': forms.Textarea(attrs={'class': 'form-control'})
#
#         }
