import django_filters
from django.forms import DateInput
from django_filters import DateFilter
from .models import Post


class PostFilter(django_filters.FilterSet):
    date_time_auto = DateFilter(lookup_expr='lte', widget=DateInput(attrs={'type': 'date'}), label='Date Filter')

    class Meta:
        model = Post
        fields = {
            'category': ['exact'],
            'choice_category': ['exact'],
            'rating': ['gt'],

        }
