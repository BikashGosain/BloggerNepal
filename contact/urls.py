from django.urls import path
from .views import contact_view

urlpatterns = [
    path('contacthome/', contact_view, name='contacthome'),
]
