from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PostDetail, PostList, Profile, PostCreate, PostUpdate, PostDelete ,like_post

urlpatterns = [
    path('', cache_page(5)(PostList.as_view()), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/like', like_post, name='like_post'),
    path('profile/', Profile.as_view(), name='profile'),

]