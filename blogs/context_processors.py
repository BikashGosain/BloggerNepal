from inymce.django.core.paginator import Paginator
from .models import Category, Notification
from social_links.models import SocialLinks
from .models import Blog
from django.db.models import Count


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


def unread_notifications_count(request):
    """
    Context processor to make unread notification count available in all templates
    """
    if request.user.is_authenticated:
        is_manager_editor = (
            request.user.groups.filter(name__in=['Manager', 'Editor']).exists() 
            or request.user.is_staff
        )
        
        if is_manager_editor:
            # Count notifications not marked as read by this admin
            unread_count = Notification.objects.exclude(
                deleted_by_admins=request.user
            ).exclude(
                read_by_admins=request.user
            ).count()
        else:
            # Count unread notifications for regular user
            unread_count = request.user.notifications.filter(
                read=False
            ).exclude(
                deleted_by_users=request.user
            ).count()
        
        return {'unread_count': unread_count}
    
    return {'unread_count': 0}


def latestpost(request):
    """Provides paginated latest published blogs to all templates."""
    latestpost = Blog.objects.filter(status='Published').order_by('-created_at')
    current_path = request.path
    
    # Set different pagination based on page
    if current_path == '/' or current_path == '/home/':
        per_page = 5  # Home page shows 5
    else:
        per_page = 9
    paginator = Paginator(latestpost, per_page)
    page_number = request.GET.get('page', 1)
    blogs_page = paginator.get_page(page_number)
    return {
        'latestpost': blogs_page
    }
