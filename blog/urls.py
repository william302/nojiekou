from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('comments/<int:comment_id>/', views.reply, name='reply'),
]
