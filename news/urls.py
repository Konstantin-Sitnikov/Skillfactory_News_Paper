from django.urls import path
from .views import PostList, PostDetail, PostSearch, NewsCreate, ArticleCreate, NewsUpdate, ArticleUpdate


urlpatterns = [

   path('', PostList.as_view(), name="news_list"),
    path('search/', PostSearch.as_view(), name="news_search"),
    path('news/create/', NewsCreate.as_view(), name="news_create"),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name="news_edit"),


    path('article/create/', ArticleCreate.as_view(), name="article_create"),
    path('article/<int:pk>/edit/', NewsUpdate.as_view(), name="article_edit"),
    path('<int:pk>', PostDetail.as_view(), name="news_detail"),
]