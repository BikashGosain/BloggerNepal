from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.about_us, name='about_us'),
     path('api/', include('about_us.api_urls')),
]