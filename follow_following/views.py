from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from blogs.models import Blog
from .models import Follow
from django.core.paginator import Paginator

from django.db.models import Q

# FOLLOW USER
@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    # Prevent following self
    if request.user != user_to_follow:
        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

    # Redirect back to previous page
    return redirect(request.META.get('HTTP_REFERER', '/'))


# UNFOLLOW USER
@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)

    Follow.objects.filter(
        follower=request.user,
        following=user_to_unfollow
    ).delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))


# FOLLOWERS LIST (private, logged-in user) of dashboard profile
@login_required
def followers_list(request, username):
    return render(request, 'followers_list.html')


# FOLLOWING LIST (private, logged-in user) of dashboard profile
@login_required
def following_list(request, username):
    return render(request, 'following_list.html')

# My posts (private, logged-in user) of dashboard profile
def mypost(request):
    return render(request, 'My_Posts.html')

# Public Profile View
def profile(request, username):
    """
    Display public profile for any user with tabs (posts, followers, following)
    """
    user_obj = get_object_or_404(User, username=username)
    
    # Get the active tab
    tab = request.GET.get('tab', 'posts')
    search_query = request.GET.get('search', '').strip()

    # Check if logged-in user follows this user
    is_following = False
    if request.user.is_authenticated and request.user != user_obj:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user_obj
        ).exists()

    # Get user's following IDs (for follow/unfollow buttons in lists)
    user_following_ids = []
    if request.user.is_authenticated:
        user_following_ids = list(
            Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
        )

    # Initialize context
    context = {
        'user_obj': user_obj,
        'is_following': is_following,
        'tab': tab,
        'search': search_query,
        'user_following_ids': user_following_ids,
    }

    # Handle different tabs
    if tab == 'followers':
        # Followers tab
        followers_qs = Follow.objects.filter(following=user_obj).select_related('follower')
        
        if search_query:
            followers_qs = followers_qs.filter(follower__username__icontains=search_query)
        
        paginator = Paginator(followers_qs, 2)
        page_number = request.GET.get('page', 1)
        followers = paginator.get_page(page_number)
        
        context['followers'] = followers
        
    elif tab == 'following':
        # Following tab
        following_qs = Follow.objects.filter(follower=user_obj).select_related('following')
        
        if search_query:
            following_qs = following_qs.filter(following__username__icontains=search_query)
        
        paginator = Paginator(following_qs, 2)
        page_number = request.GET.get('page', 1)
        following = paginator.get_page(page_number)
        
        context['following'] = following
        
    else:
        # Posts tab (default)
        posts_qs = Blog.objects.filter(author=user_obj, status='Published').order_by('-created_at')
        
        if search_query:
            posts_qs = posts_qs.filter(
                Q(title__icontains=search_query) | 
                Q(short_description__icontains=search_query)
            )
        
        paginator = Paginator(posts_qs, 2)
        page_number = request.GET.get('page', 1)
        posts = paginator.get_page(page_number)
        
        context['posts'] = posts
        context['posts_count'] = Blog.objects.filter(author=user_obj, status='Published').count()

    return render(request, 'public_profile.html', context)


# 2️⃣ Public Followers List (KEEP for backward compatibility - redirects to profile with tab)
def public_followers_list(request, username):
    """
    Redirect to profile page with followers tab
    """
    return redirect(f'/profile/{username}/?tab=followers')


# 3️⃣ Public Following List (KEEP for backward compatibility - redirects to profile with tab)
def public_following_list(request, username):
    """
    Redirect to profile page with following tab
    """
    return redirect(f'/profile/{username}/?tab=following')