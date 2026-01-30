from django.contrib.auth.models import User
from .models import Follow

def user_following_ids(request):
    """
    IDs of users that the logged-in user is following
    """
    user = getattr(request, 'user', None)
    if user and getattr(user, 'is_authenticated', False):
        following_ids = Follow.objects.filter(
            follower=user
        ).values_list('following_id', flat=True)
    else:
        following_ids = []

    return {
        'user_following_ids': list(following_ids)
    }


def follow_counts(request):
    user = getattr(request, 'user', None)
    if user and getattr(user, 'is_authenticated', False):
        return {
            'my_followers_count': Follow.objects.filter(following=user).count(),
            'my_following_count': Follow.objects.filter(follower=user).count(),
        }
    return {
        'my_followers_count': 0,
        'my_following_count': 0,
    }


def followers_list(request):
    """
    Followers of a user specified in the URL: /profile/<username>/
    """
    if not getattr(request, 'resolver_match', None):
        return {}

    username = request.resolver_match.kwargs.get('username', None)
    if not username:
        return {}

    user_obj = User.objects.filter(username=username).first()
    if not user_obj:
        return {
            'follow_error': 'User does not exist.',
            'followers': [],
        }

    followers = Follow.objects.filter(
        following=user_obj
    ).select_related('follower')

    search_query = request.GET.get('search', '').strip()
    if search_query:
        followers = followers.filter(
            follower__username__icontains=search_query
        )

    return {
        'user_obj': user_obj,
        'followers': followers,
        'search_query': search_query,
    }


def following_list(request):
    """
    Users that a user is following, based on URL: /profile/<username>/
    """
    if not getattr(request, 'resolver_match', None):
        return {}

    username = request.resolver_match.kwargs.get('username', None)
    if not username:
        return {}

    user_obj = User.objects.filter(username=username).first()
    if not user_obj:
        return {
            'follow_error': 'User does not exist.',
            'following': [],
        }

    following = Follow.objects.filter(
        follower=user_obj
    ).select_related('following')

    search_query = request.GET.get('search', '').strip()
    if search_query:
        following = following.filter(
            following__username__icontains=search_query
        )

    return {
        'user_obj': user_obj,
        'following': following,
        'search_query': search_query,
    }
