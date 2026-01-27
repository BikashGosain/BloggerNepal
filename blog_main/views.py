import random
from django.shortcuts import get_object_or_404, render, redirect
from blogs.models import Blog, Category
from about_us.models import AboutUs
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.db.models import Count
from django.core.paginator import Paginator

def home(request):
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status='Published')
    paginator = Paginator(featured_posts, 6)
    page = request.GET.get('page', 1)
    blogs_page = paginator.get_page(page)

    posts = Blog.objects.filter(is_featured=False, status='Published').order_by('-created_at')

    # Fetch About Us information
    try:
        about = AboutUs.objects.get()
    except:
        about = None

    context = {
        # 'categories': categories, # removed as we are using context processor for categories
        'featured_posts': blogs_page,
        'posts': posts,
        'about': about,
    }
    return render(request, 'home.html', context)
        

def randomblogs(request):
    blogs = Blog.objects.filter(status='Published').order_by('?')
    
    paginator = Paginator(blogs, 9)
    page = request.GET.get('page', 1)
    blogs_page = paginator.get_page(page)

    context = {
        'randomblogs': blogs_page,
    }
    
    return render(request, 'randomblogs.html', context)

def latestpost(request):
    return render(request, 'latestpost.html')

def popularpost(request):
    popularpost = Blog.objects.filter(
        status='Published'
    ).annotate(
        like_count=Count('likes')
    ).order_by('-views', '-like_count')
    paginator = Paginator(popularpost, 9)
    page = request.GET.get('page', 1)
    blogs_page = paginator.get_page(page)

    context = {
        'popularpost': blogs_page,
    }
    return render(request, 'popularpost.html', context)

def category(request):
    return render(request, 'category.html')

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