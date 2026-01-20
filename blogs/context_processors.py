from .models import Category
from social_links.models import SocialLinks


def get_categories(request):
    
    categories = Category.objects.all()
    return dict(categories=categories)

def get_social_links(request):
    social_links = SocialLinks.objects.all()
    return dict(social_links=social_links)

def user_roles(request):
    user = request.user
    can_see_all = False
    if user.is_authenticated:
        can_see_all = user.is_superuser or user.groups.filter(name__in=['Editor', 'Manager']).exists()
    return {
        'can_see_all': can_see_all,
        'current_user': user
    }
