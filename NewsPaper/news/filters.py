import django_filters
from django.forms import DateInput
from django_filters import FilterSet
from .models import Post


class NewsFilter(FilterSet):
    post_creation_datetime__gt = django_filters.DateFilter(
        field_name='post_creation_datetime__date',
        lookup_expr='gt',
        label='Новость позже даты: ',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'author__author__username': ['icontains'],
            'post_creation_datetime': [],
        }
