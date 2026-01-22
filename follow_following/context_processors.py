def follow_counts(request):
    if request.user.is_authenticated:
        return {
            'my_followers_count': request.user.followers.count(),
            'my_following_count': request.user.following.count(),
        }
    return {}
