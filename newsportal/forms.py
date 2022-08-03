from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group

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


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
