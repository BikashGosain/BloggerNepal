from django.shortcuts import get_object_or_404, render, redirect
from blogs.models import Blog, Category
from about_us.models import AboutUs
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.db.models import Count

def home(request):
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status='Published')
    posts = Blog.objects.filter(is_featured=False, status='Published').order_by('-created_at')

    # Fetch About Us information
    try:
        about = AboutUs.objects.get()
    except:
        about = None

    context = {
        # 'categories': categories, # removed as we are using context processor for categories
        'featured_posts': featured_posts,
        'posts': posts,
        'about': about,
    }
    return render(request, 'home.html', context)
    
def latestpost(request):
    return render(request, 'latestpost.html')

def popularpost(request):
    return render(request, 'popularpost.html')

def about(request):
    about = AboutUs.objects.get()
    context = {
        'about': about,
    }
    return render(request, 'about.html', context)
def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
        
            # You can add a success message or redirect to login page
    context = {
        'form': form,
        }
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')