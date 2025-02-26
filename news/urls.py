from django.urls import path
from .views import (PostList, PostDetail, PostSearch,PublicationCreate, PublicationUpdate,
                    PublicationDelete,
                    edit_delete_invalid,
                    like_dislike, CategoryList, subscribe
                    )


urlpatterns = [

    path('', PostList.as_view(), name="news_list"),
    path('search/', PostSearch.as_view(), name="news_search"),
    path('<int:pk>', PostDetail.as_view(), name="news_detail"),

    path('news/create/', PublicationCreate.as_view(), name="news_create"),
    path('news/<int:pk>/edit/', PublicationUpdate.as_view(), name="news_edit"),
    path('news/<int:pk>/delete/', PublicationDelete.as_view(), name="news_delete"),
    path('edit_delete_error/', edit_delete_invalid, name="edit_delete_error"),

    path('article/create/', PublicationCreate.as_view(), name="article_create"),
    path('article/<int:pk>/edit/', PublicationUpdate.as_view(), name="article_edit"),
    path('article/<int:pk>/delete/', PublicationDelete.as_view(), name="article_delete"),
    path('<int:pk>/like_dislike/', like_dislike, name="like_dislike"),

    path('categories/<int:pk>', CategoryList.as_view(), name="category_list"),

    path('categories/<int:pk>/subscribe', subscribe, name="subscribe"),



]