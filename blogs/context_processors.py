from .models import Category
from social_links.models import SocialLinks
from .models import Blog


def get_categories(request):
    
    categories = Category.objects.all()
    return dict(categories=categories)

def get_social_links(request):
    social_links = SocialLinks.objects.all()
    return dict(social_links=social_links)


def user_roles(request):
    user = request.user
    can_see_all = False
    blogs_count = 0
    self_posts_count = 0
    is_editor = False
    is_manager = False

    if user.is_authenticated:
        can_see_all = user.is_superuser or user.groups.filter(name__in=['Admin', 'Manager', 'Editor']).exists()
        is_editor = user.groups.filter(name='Editor').exists()
        is_manager = user.groups.filter(name='Manager').exists()
        
        if can_see_all:
            blogs_count = Blog.objects.count()
        self_posts_count = Blog.objects.filter(author=user).count()

    return {
        'can_see_all': can_see_all,
        'is_editor': is_editor,
        'is_manager': is_manager,
        'current_user': user,
        'blogs_count': blogs_count,
        'self_posts_count': self_posts_count
    }


