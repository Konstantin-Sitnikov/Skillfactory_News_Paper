from django.urls import path
from .views import PostList, PostDetail, PostSearch


urlpatterns = [

   path('', PostList.as_view(), name="news_list"),
    path('search/', PostSearch.as_view(), name="news_search"),
    path('<int:pk>', PostDetail.as_view()),
]