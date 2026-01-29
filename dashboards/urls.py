from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
# blogs app ko view bata funtion called: notifications
from blogs import views as notification_views


urlpatterns = [
    # Dashboard Home
    path('', login_required(views.dashboard, login_url='login'), name='dashboard'),
    path('analytics/category/', login_required(views.posts_per_category, login_url='login'), name='posts_per_category'),
    path('analytics/month/', login_required(views.posts_per_month, login_url='login'), name='posts_per_month'),

    # Category CRUD
    path('categories/', login_required(views.categories, login_url='login'), name='categories'),
    path('categories/add/', login_required(views.add_category, login_url='login'), name='add_category'),
    path('categories/edit/<int:pk>/', login_required(views.edit_category, login_url='login'), name='edit_category'),
    path('categories/delete/<int:pk>/', login_required(views.delete_category, login_url='login'), name='delete_category'),

    # Blog post CRUD
    path('posts/', login_required(views.posts, login_url='login'), name='posts'),
    path('posts/add/', login_required(views.add_post, login_url='login'), name='add_post'),
    path('posts/edit/<int:pk>/', login_required(views.edit_post, login_url='login'), name='edit_post'),
    path('posts/delete/<int:pk>/', login_required(views.delete_post, login_url='login'), name='delete_post'),
    
    # users management by manager and admin through dashboard
    path('users/', login_required(views.users, login_url='login'), name='users'),
    path('users/add/', login_required(views.add_user, login_url='login'), name='add_user'),
    path('users/edit/<int:pk>/', login_required(views.edit_user, login_url='login'), name='edit_user'),
    path('users/delete/<int:pk>/', login_required(views.delete_user, login_url='login'), name='delete_user'),
    # profile
    path('profile/', login_required(views.profile, login_url='login'), name='profile'),
    path('profile/edit/', login_required(views.edit_profile, login_url='login'), name='edit_profile'),

    path(
    'dashboardnotification/',
    login_required(
        notification_views.notifications,
        login_url='login'
    ),
    name='dashboardnotification'
),

    path('dashboardfollowers_list/<str:username>/', login_required(views.dashboardfollowers_list, login_url='login'), name='dashboardfollowers_list'),
    path('dashboardfollowing_list/<str:username>/', login_required(views.dashboardfollowing_list, login_url='login'), name='dashboardfollowing_list'),

]