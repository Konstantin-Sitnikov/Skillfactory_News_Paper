from django.urls import path
from .views import PostList, PostDetail, PostSearch, NewsCreate, ArticleCreate


urlpatterns = [

   path('', PostList.as_view(), name="news_list"),
    path('search/', PostSearch.as_view(), name="news_search"),
    path('news/create/', NewsCreate.as_view(), name="news_create"),
    path('article/create/', NewsCreate.as_view(), name="article_create"),
    path('<int:pk>', PostDetail.as_view(), name="news_detail"),
]