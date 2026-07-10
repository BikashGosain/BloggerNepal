from django.urls import path
from blogs import views

urlpatterns = [
    path(
    'api/blogs/',
    views.blog_api,
    name='blog_api'
),
    path('<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    # for like and dislike and report
    path('like/<int:blog_id>/', views.blog_like, name='blog_like'),
    path('dislike/<int:blog_id>/', views.blog_dislike, name='blog_dislike'),
    path('report/<int:blog_id>/', views.report_blog, name='report_blog'),
    # for notification
    path('notifications/', views.notifications, name='notifications'),


# for blog summary
    path(
    'summary/<slug:slug>/',
    views.blog_summary,
    name='blog_summary'
),
]