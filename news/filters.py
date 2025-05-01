from tokenize import group

import django_filters
from django_filters import FilterSet
from django import forms
from .models import Post, Category, Author
from django.contrib.auth.models import User, Group


class NewsFilter(FilterSet):
    autor_id = django_filters.ModelChoiceFilter(queryset=Author.objects.all(), label="Автор")
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label="Категория")
    title_news = django_filters.CharFilter(lookup_expr='icontains', label="Название статьи")
    date_time = django_filters.DateFilter(field_name="date_time", lookup_expr='gt', label="Дата", widget=forms.DateInput(attrs={"type": 'date'}))

    class Meta:
        model = Post

        fields = [

       ]

