from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.PostList.as_view(), name='postlist'),
    path('api/<int:pk>/', views.PostDetail.as_view(), name='postdetail'),
    path('posts/<int:post_id>/', views.detail, name='detail'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('comments/<int:comment_id>/', views.reply, name='reply'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('posts_all', views.posts, name='posts'),
    path('category/<int:category_id>', views.category, name='category'),
]
