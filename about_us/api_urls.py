from django.urls import path
from .api_views import AboutUsListAPIView

urlpatterns = [
    path('', AboutUsListAPIView.as_view(), name='about-us-api'),
]
