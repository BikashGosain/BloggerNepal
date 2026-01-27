from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from blogs.models import Blog
from .models import Follow
from django.core.paginator import Paginator

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


# FOLLOWERS LIST
@login_required
def followers_list(request, username):
    user_obj = get_object_or_404(User, username=username)

    followers = Follow.objects.filter(
        following=user_obj
    ).select_related('follower')

    # IDs of users current logged-in user is following
    user_following_ids = []
    if request.user.is_authenticated:
        user_following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)

    return render(request, 'followers_list.html', {
        'user_obj': user_obj,
        'followers': followers,
        'user_following_ids': list(user_following_ids),
    })


# FOLLOWING LIST
@login_required
def following_list(request, username):
    user_obj = get_object_or_404(User, username=username)

    following = Follow.objects.filter(
        follower=user_obj
    ).select_related('following')

    # IDs of users current logged-in user is following
    user_following_ids = []
    if request.user.is_authenticated:
        user_following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)

    return render(request, 'following_list.html', {
        'user_obj': user_obj,
        'following': following,
        'user_following_ids': list(user_following_ids),
    })


def profile(request, username):
    """
    Display public profile for any user
    """
    user_obj = get_object_or_404(User, username=username)

    posts = Blog.objects.filter(author=user_obj).order_by('-created_at')
    paginator = Paginator(posts, 6)
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

def mypost(request):
    user = request.user
    posts = Blog.objects.filter(author=user)

    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'My_Posts.html', context)