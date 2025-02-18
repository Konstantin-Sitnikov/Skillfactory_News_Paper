from django.urls import path
from .views import IndexView, LogoutView, upgrade_me

urlpatterns = [
    path('login/', IndexView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('upgrade/', upgrade_me, name = 'upgrade'),

]