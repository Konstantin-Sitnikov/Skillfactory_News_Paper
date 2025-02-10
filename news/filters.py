from django_filters import FilterSet
from .models import Post

class NewsFilter(FilterSet):
   class Meta:
       model = Post

       fields = {
           # поиск по автору
           'autor_id__user': ['in'],
           # поиск но новости
           'title_news': ['icontains'],
           #поиск по дате
           'date_time': ['year__gt'],
       }