from django.shortcuts import render
from .models import AboutUs
# Create your views here.

def about_us(request):
    about = AboutUs.objects.all().order_by('created_at')  # or 'created_at' if you prefer
    context = {
        'about': about
    }
    return render(request, 'about_us.html', context)