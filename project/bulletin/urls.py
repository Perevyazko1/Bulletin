from django.urls import path
from django.views.decorators.cache import cache_page

from .views import NewsDetail, NewsList, Profile, PostCreate

urlpatterns = [
    path('', cache_page(5)(NewsList.as_view()), name='news_list'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('profile/', Profile.as_view(), name='profile'),

]