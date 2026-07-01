from django.core.paginator import Paginator
from .models import Category,Blog, Notification
from social_links.models import SocialLinks
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.contrib import messages


def get_categories(request):
    # 🔹 Get search query from URL
    search_query = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)

    categories_qs = Category.objects.annotate(
        blog_count=Count(
            'blog',
            filter=Q(blog__status='Published')
        )
    ).order_by('category_name')

    # 🔹 Apply search if query exists
    if search_query:
        categories_qs = categories_qs.filter(
            category_name__icontains=search_query
        )

    paginator = Paginator(categories_qs, 4)
    page_obj = paginator.get_page(page_number)

    uncategorized_count = Blog.objects.filter(
        category__isnull=True,
        status='Published'
    ).count()

    return {
        'categories': page_obj,          # paginated categories with blog_count
        'uncategorized_count': uncategorized_count,
        'category_search': search_query,
    }


def get_social_links(request):
    social_links = SocialLinks.objects.all()
    return {
        'social_links': social_links
    }



def user_roles(request):
    # Use getattr to safely get user; returns None if user doesn't exist
    user = getattr(request, 'user', None)

    can_see_all = False
    blogs_count = 0
    self_posts_count = 0
    is_editor = False
    is_manager = False

    if user and getattr(user, 'is_authenticated', False):
        # Admin / Editor / Manager check
        can_see_all = user.is_superuser or user.groups.filter(name__in=['Admin', 'Manager', 'Editor']).exists()
        is_editor = user.groups.filter(name='Editor').exists()
        is_manager = user.groups.filter(name='Manager').exists()

        # Count blogs
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


from blogs.models import Notification

def unread_notifications_count(request):
    """
    Context processor to make unread notification count available in all templates
    Safely handles cases when request.user may not exist (e.g., 404/500 pages)
    """
    user = getattr(request, 'user', None)
    
    unread_count = 0  # default if no user or anonymous

    if user and getattr(user, 'is_authenticated', False):
        is_manager_editor = (
            user.groups.filter(name__in=['Manager', 'Editor']).exists()
            or user.is_staff
        )

        if is_manager_editor:
            # Count notifications not marked as read by this admin
            unread_count = Notification.objects.exclude(
                deleted_by_admins=user
            ).exclude(
                read_by_admins=user
            ).count()
        else:
            # Count unread notifications for regular user
            unread_count = user.notifications.filter(
                read=False
            ).exclude(
                deleted_by_users=user
            ).count()

    return {'unread_count': unread_count}



def latestpost(request):
    """Provides paginated latest published blogs to all templates."""
    latestpost = Blog.objects.filter(status='Published').order_by('-created_at')

    current_path = request.path
    
    # Set different pagination based on page
    if current_path == '/' or current_path == '/home/':
        per_page = 6  # Home page shows 5
    else:
        per_page = 24
    paginator = Paginator(latestpost, per_page)
    page_number = request.GET.get('page', 1)
    blogs_page = paginator.get_page(page_number)
    return {
        'latestpost': blogs_page
    }
