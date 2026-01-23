from django.urls import path
from . import views

urlpatterns = [
    # Follow / Unfollow
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),

    # Followers / Following lists
    path('<str:username>/followers/', views.followers_list, name='followers_list'),
    path('<str:username>/following/', views.following_list, name='following_list'),

    # **Public profile view for any user**
    path('profile/<str:username>/', views.profile, name='profile'),
    path('mypost', views.mypost, name='mypost'),

]
