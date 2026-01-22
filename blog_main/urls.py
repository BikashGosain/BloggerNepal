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
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from blogs import views as BlogsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('category/', include('blogs.urls')),
    path('blog/search/', BlogsView.search, name='search'),
    path('blog/<slug:slug>/', BlogsView.blogs, name='blogs'),
    

    # authentication, authorization urls and permissions
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Dashboard URLs
    path('dashboard/', include('dashboards.urls')),
    # TinyMCE (REQUIRED)
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # for contact email
    path('', include('contact.urls')),

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
