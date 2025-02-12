import django_filters
from django_filters import FilterSet
from django import forms
from .models import Post



class NewsFilter(FilterSet):
    autor_id__user__username = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='type')
    title_news = django_filters.CharFilter(lookup_expr='icontains')
    date_time = django_filters.DateFilter(field_name="date_time", lookup_expr='gt', label="Date", widget=forms.DateInput(attrs={"type": 'date'}))

    class Meta:
        model = Post

        fields = [ "autor_id__user__username",
                   "title_news",
                   "date_time"


       ]

