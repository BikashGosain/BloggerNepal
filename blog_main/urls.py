"""
URL configuration for blog_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from blogs import views as BlogsView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),
    
    path('', views.home, name='home'),

    path('randomblogs/', views.randomblogs, name='randomblogs'),
    path('latestpost/', views.latestpost, name='latestpost'),
    path('popularpost/', views.popularpost, name='popularpost'),
    path('category/', views.category, name='category'),

    path('about_us/', include('about_us.urls')),
    
    path('contact/', views.contact, name='contact'),

    path('category/', include('blogs.urls')),
    path('blog/search/', BlogsView.search, name='search'),
    path('blog/<slug:slug>/', BlogsView.blogs, name='blogs'),
    

    # authentication, authorization urls and permissions
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Dashboard URLs
    path('dashboard/', include('dashboards.urls')),
# for image uploads
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # for contact email
    path('', include('contact.urls')),

    path('accounts/', include('follow_following.urls')),
    # for global error page redirection if page not exit
    # re_path(r'^.*$', views.page_not_found_redirect)
    

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )

# 👇 custom 404 handler
handler404 = 'blog_main.views.custom_404'
handler400 = 'blog_main.views.custom_400'
handler403 = 'blog_main.views.custom_403'
handler500 = 'blog_main.views.custom_500'


