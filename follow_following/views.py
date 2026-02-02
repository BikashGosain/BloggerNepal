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

# 1️⃣ My posts (private, logged-in user) of dashboard profile
def mypost(request):
    return render(request, 'My_Posts.html')

# 1️⃣ Public Profile View
def profile(request, username):
    """
    Display public profile for any user
    """
    user_obj = get_object_or_404(User, username=username)

    posts = Blog.objects.filter(author=user_obj).order_by('-created_at')
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)

    # Check if logged-in user follows this user
    is_following = False
    if request.user.is_authenticated and request.user != user_obj:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user_obj
        ).exists()

    context = {
        'user_obj': user_obj,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'public_profile.html', context)


# 2️⃣ Public Followers List
def public_followers_list(request, username):
    user_obj = get_object_or_404(User, username=username)
    search_query = request.GET.get('search', '').strip()

    followers_qs = Follow.objects.filter(following=user_obj).select_related('follower')

    if search_query:
        followers_qs = followers_qs.filter(follower__username__icontains=search_query)

    followers = Paginator(followers_qs, 10).get_page(request.GET.get('page'))

    return render(request, 'public_followers_list.html', {
        'user_obj': user_obj,
        'followers': followers,
        'search': search_query,   # pass to template
    })


# 3️⃣ Public Following List
def public_following_list(request, username):
    user_obj = get_object_or_404(User, username=username)
    search_query = request.GET.get('search', '').strip()

    following_qs = Follow.objects.filter(follower=user_obj).select_related('following')

    if search_query:
        following_qs = following_qs.filter(following__username__icontains=search_query)

    following = Paginator(following_qs, 10).get_page(request.GET.get('page'))

    return render(request, 'public_following_list.html', {
        'user_obj': user_obj,
        'following': following,
        'search': search_query,   # pass to template
    })
