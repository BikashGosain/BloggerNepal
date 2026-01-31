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
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

def home(request):
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('-created_at')
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
        'categories': categories,
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
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            # Check if there's an inactive user with this username/email
            user = User.objects.filter(username=username, email=email, is_active=False).first()

            if not user:
                # Create new user
                user = form.save(commit=False)
                user.is_active = False
                user.save()
            else:
                # Update the password for the existing inactive user
                user.set_password(form.cleaned_data['password1'])
                user.save()

            otp = random.randint(100000, 999999)
            request.session['otp'] = str(otp)
            request.session['user_id'] = user.id

            send_mail(
                'OTP Verification',
                f'Your OTP is {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return redirect('verify_otp')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def verify_otp(request):
    user_id = request.session.get('user_id')
    session_otp = request.session.get('otp')

    if not user_id or not session_otp:
        return redirect('register')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if entered_otp == str(session_otp):
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            request.session.pop('otp', None)
            request.session.pop('user_id', None)
            return redirect('login')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html')

def resend_otp(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('register')

    user = User.objects.get(id=user_id)

    otp = random.randint(100000, 999999)
    request.session['otp'] = str(otp)

    send_mail(
        'OTP Verification (Resent)',
        f'Your OTP is {otp}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    return redirect('verify_otp')

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


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email, is_active=True)
            
            # Generate OTP
            otp = random.randint(100000, 999999)
            request.session['reset_otp'] = str(otp)
            request.session['reset_user_id'] = user.id
            
            # Send OTP via email
            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'OTP has been sent to your email.')
            return redirect('verify_reset_otp')
            
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
    
    return render(request, 'forgot_password.html')


def verify_reset_otp(request):
    reset_user_id = request.session.get('reset_user_id')
    session_otp = request.session.get('reset_otp')
    
    if not reset_user_id or not session_otp:
        messages.error(request, 'Invalid session. Please try again.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        if entered_otp == str(session_otp):
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    return render(request, 'verify_reset_otp.html')


def reset_password(request):
    reset_user_id = request.session.get('reset_user_id')
    
    if not reset_user_id:
        messages.error(request, 'Invalid session. Please try again.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'reset_password.html')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'reset_password.html')
        
        try:
            user = User.objects.get(id=reset_user_id)
            user.set_password(password1)
            user.save()
            
            # Clear session
            request.session.pop('reset_otp', None)
            request.session.pop('reset_user_id', None)
            
            messages.success(request, 'Password reset successful! Please login with your new password.')
            return redirect('login')
            
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('forgot_password')
    
    return render(request, 'reset_password.html')


def resend_reset_otp(request):
    reset_user_id = request.session.get('reset_user_id')
    
    if not reset_user_id:
        messages.error(request, 'Invalid session. Please try again.')
        return redirect('forgot_password')
    
    try:
        user = User.objects.get(id=reset_user_id)
        
        # Generate new OTP
        otp = random.randint(100000, 999999)
        request.session['reset_otp'] = str(otp)
        
        # Send OTP via email
        send_mail(
            'Password Reset OTP (Resent)',
            f'Your new OTP for password reset is: {otp}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
        messages.success(request, 'A new OTP has been sent to your email.')
        
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('forgot_password')
    
    return redirect('verify_reset_otp')

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

