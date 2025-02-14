from django.urls import path
from .views import (PostList, PostDetail, PostSearch,PublicationCreate,
                    NewsUpdate,NewsDelete,
                    ArticleUpdate, ArticleDelete,
                    news_update_delete_invalid,
                    article_update_delete_invalid)


urlpatterns = [



    path('', PostList.as_view(), name="news_list"),
    path('search/', PostSearch.as_view(), name="news_search"),
    path('<int:pk>', PostDetail.as_view(), name="news_detail"),

    path('news/create/', PublicationCreate.as_view(), name="news_create"),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name="news_edit"),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name="news_delete"),
    path('newsediterror/', news_update_delete_invalid, name="newsediterror"),


    path('article/create/', PublicationCreate.as_view(), name="article_create"),
    path('article/<int:pk>/edit/', ArticleUpdate.as_view(), name="article_edit"),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name="article_delete"),
    path('articleediterror/', article_update_delete_invalid, name="articleediterror"),






]