from django.urls import path
from . import views

urlpatterns = [
    
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('<str:username>/followers/', views.followers_list, name='followers_list'),
    path('<str:username>/following/', views.following_list, name='following_list'),
]
