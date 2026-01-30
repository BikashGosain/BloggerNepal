from blogs.models import Blog, Category

def dashboard_header_context(user):
    is_manager = user.groups.filter(name='Manager').exists()
    can_see_all = is_manager or user.is_superuser

    category_count = Category.objects.count() if can_see_all else (
        Category.objects.filter(blog__author=user).distinct().count()
    )

    blogs_count = Blog.objects.count() if can_see_all else (
        Blog.objects.filter(author=user).count()
    )

    self_posts_count = Blog.objects.filter(author=user).count()
    self_posts_uncategorized_count = Blog.objects.filter(author=user, category__isnull=True).count()

    all_posts_uncategorized_count = Blog.objects.filter(category__isnull=True).count()

    return {
        'can_see_all': can_see_all,
        'category_count': category_count,
        'blogs_count': blogs_count,
        'self_posts_count': self_posts_count,
        'self_posts_uncategorized_count': self_posts_uncategorized_count,
        'all_posts_uncategorized_count': all_posts_uncategorized_count,
    }


