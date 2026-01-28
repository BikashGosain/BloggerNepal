from django.contrib.auth.models import User
from .models import Follow

def user_following_ids(request):
    """
    IDs of users that the logged-in user is following
    """
    if request.user.is_authenticated:
        following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)
    else:
        following_ids = []

    return {
        'user_following_ids': list(following_ids)
    }

def follow_counts(request):
    if request.user.is_authenticated:
        return {
            'my_followers_count': Follow.objects.filter(following=request.user).count(),
            'my_following_count': Follow.objects.filter(follower=request.user).count(),
        }
    return {}


def followers_list(request):
    if not request.resolver_match:
        return {}

    username = request.resolver_match.kwargs.get('username')
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
    if not request.resolver_match:
        return {}

    username = request.resolver_match.kwargs.get('username')
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
