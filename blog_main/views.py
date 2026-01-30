import random
from django.shortcuts import get_object_or_404, render, redirect
from blogs.models import Blog, Category
from about_us.models import AboutUs
from django.contrib import messages
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
    about = AboutUs.objects.all()[:3]

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

# def page_not_found_redirect(request, *args, **kwargs):
#     # Add a warning message
#     messages.warning(request, "The page you tried to visit does not exist.")
#     # Redirect to home
#     return redirect('home')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_400(request, exception):
    return render(request, '400.html', status=400)

def custom_403(request, exception):
    return render(request, '403.html', status=403)

def custom_500(request):
    return render(request, '500.html', status=500)

