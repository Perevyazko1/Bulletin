from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PostDetail, PostList, Profile, PostCreate, PostUpdate, PostDelete, ResponseCreate, \
    user_response, accept_response, delete_response

urlpatterns = [
    path('', cache_page(5)(PostList.as_view()), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/response', ResponseCreate.as_view(), name='response'),
    path('<int:pk>/delete_response', delete_response, name='delete_response'),
    path('<int:pk>/user_response', user_response, name='user_response'),
    path('<int:pk>/accept_response', accept_response, name='accept_response'),
    path('profile/', Profile.as_view(), name='profile'),

]