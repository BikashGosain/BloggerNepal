from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from follow_following.models import Follow
from inymce.django.core.paginator import Paginator
from .models import Blog, Category, Comment, Notification, Report
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

def posts_by_category(request, category_id):
    if int(category_id) == 0:  # Special case: Uncategorized
        category = None
        posts_qs = Blog.objects.filter(category__isnull=True, status='Published').order_by('-created_at')
        category_name = "Uncategorized"
    else:
        category = get_object_or_404(Category, id=category_id)
        posts_qs = Blog.objects.filter(category=category, status='Published').order_by('-created_at')
        category_name = category.category_name

    paginator = Paginator(posts_qs, 24)
    page_number = request.GET.get('page', 1)
    posts_page = paginator.get_page(page_number)

    context = {
        'posts_by_category': posts_page,
        'category': category,
        'category_name': category_name
    }

    return render(request, 'posts_by_category.html', context)


def blogs(request, slug):
    user = request.user
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    all_posts = Blog.objects.filter(status='Published').exclude(id=single_blog.id)
    
    # Call the function with both arguments
    similar_posts = get_similar_posts(single_blog, all_posts, limit=5)
    # 🔔 MARK NOTIFICATION AS READ (if coming from notification link)
    notification_id = request.GET.get("notification")
    if request.user.is_authenticated and notification_id:
        notification = Notification.objects.filter(
            id=notification_id,
            blog=single_blog
        ).first()  # safely get or None
        if notification:
            # Admin/Manager/Editor: track read in their own view
            if request.user.is_staff or request.user.groups.filter(name__in=['Manager','Editor']).exists():
                notification.read_by_admins.add(request.user)
            else:
                # Normal user: mark as read
                notification.read = True
                notification.save(update_fields=['read'])

    # # Increment view count: views count when page reload also
    # single_blog.views += 1
    # single_blog.save(update_fields=['views'])
    # Increment view count (only once per session)
    single_blog.increment_view(request)

    # Check if current user is following author
    is_following = False
    if request.user.is_authenticated and request.user != single_blog.author:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=single_blog.author
        ).exists()

    # Check if user has reported this blog
    last_report = None
    user_reported = False
    can_report = False
    if request.user.is_authenticated:
        last_report = single_blog.reports.filter(user=request.user).order_by('-created_at').first()
        user_reported = last_report is not None
        # Can report if never reported or blog updated after last report
        can_report = (not user_reported) or (last_report and last_report.created_at < single_blog.updated_at)

    # Unread notification count
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.groups.filter(name__in=['Manager','Editor']).exists():
            unread_count = Notification.objects.exclude(read_by_admins=request.user).count()
        else:
            unread_count = request.user.notifications.filter(read=False).count()
    else:
        unread_count = 0

    # Handle comments
    if request.method == 'POST':
        text = request.POST.get('comment', '').strip()
        parent_id = request.POST.get('parent_id')
        if text:
            comment = Comment(blog=single_blog, user=request.user, comment=text)
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
        return redirect(request.path)

    comments = Comment.objects.filter(blog=single_blog).order_by('-created_at')
    comment_count = comments.count()

    context = {
        'single_blog': single_blog,
        'comments': comments,
        'comment_count': comment_count,
        'user': user,
        'user_reported': user_reported,
        'last_report_time': last_report.created_at if last_report else None,
        'can_report': can_report,
        'unread_count': unread_count,
        'is_following': is_following,
        'similar_posts': similar_posts,
    }

    return render(request, 'blogsdetail.html', context)

def get_similar_posts(current_post, all_posts, limit=5):
    similarity_score = {}

    for post in all_posts:
        score = 0
        if post.category == current_post.category:
            score += 3

        # Title keyword overlap
        current_words = set(current_post.title.lower().split())
        post_words = set(post.title.lower().split())
        score += len(current_words & post_words)

        similarity_score[post] = score

    similar_posts = sorted(similarity_score, key=lambda x: similarity_score[x], reverse=True)

    return similar_posts[:limit]




@login_required
def blog_like(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    user = request.user

    # Remove dislike if exists
    if user in blog.dislikes.all():
        blog.dislikes.remove(user)

    # Toggle like
    if user in blog.likes.all():
        blog.likes.remove(user)
    else:
        blog.likes.add(user)

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def blog_dislike(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    user = request.user

    # Remove like if exists
    if user in blog.likes.all():
        blog.likes.remove(user)

    # Toggle dislike
    if user in blog.dislikes.all():
        blog.dislikes.remove(user)
    else:
        blog.dislikes.add(user)

    return redirect(request.META.get('HTTP_REFERER', '/'))



@login_required
def report_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    user = request.user

    # Prevent owner from reporting their own blog
    if blog.author == user:
        messages.error(request, "You cannot report your own blog.")
        return redirect(blog.get_absolute_url())

    # Check if already reported **after last update**
    last_report = blog.reports.filter(user=user).order_by('-created_at').first()
    can_report = True
    if last_report and last_report.created_at >= blog.updated_at:
        can_report = False  # user already reported after last update

    if request.method == 'POST' and can_report:
        reason = request.POST.get('reason', '').strip()
        # Create report
        Report.objects.create(blog=blog, user=user, reason=reason if reason else None)

        # Notification for blog author
        if reason:
            message = f"Your blog '{blog.title}' has been reported. Reason: {reason}"
        else:
            message = f"Your blog '{blog.title}' has been reported."
        Notification.objects.create(user=blog.author, blog=blog, message=message)

        messages.success(request, "Report submitted.")
        return redirect(blog.get_absolute_url())

    # Pass can_report to template to decide whether to show the button
    context = {
        'blog': blog,
        'can_report': can_report
    }
    return render(request, 'blogs.html', context)





@login_required
def notifications(request):

    # Handle delete single notification
    if request.method == "POST" and "delete_one" in request.POST:
        notification_id = request.POST.get("delete_one")
        notification = Notification.objects.filter(id=notification_id).first()
        if notification:
        # Admin/Manager/Editor deletes someone else's notification
            if request.user.is_staff or request.user.groups.filter(name__in=['Manager','Editor']).exists():
                notification.deleted_by_admins.add(request.user)
            else:
            # Normal user deletes their own notification
                if notification.user == request.user:
                    notification.deleted_by_users.add(request.user)  # actually deletes for them only

        return redirect(request.path)
    

    # Handle delete all notifications
    if request.method == "POST" and "delete_all" in request.POST:
        # Admin/Manager/Editor deletes: mark deleted for themselves
        if request.user.is_staff or request.user.groups.filter(name__in=['Manager','Editor']).exists():
                for n in Notification.objects.all():
                    n.deleted_by_admins.add(request.user)
        else:
            # Normal user deletes: mark all their notifications as deleted for themselves
            for n in request.user.notifications.all():
                n.deleted_by_users.add(request.user)
        return redirect(request.path)

    # MARK SINGLE NOTIFICATION AS READ
    if request.method == "POST" and "mark_read" in request.POST:
        notification_id = request.POST.get("mark_read")
        notification = Notification.objects.get(id=notification_id)
        if request.user.groups.filter(name__in=['Manager', 'Editor']).exists() or request.user.is_superuser:
            notification.read_by_admins.add(request.user)
        else:
            notification.read = True
            notification.save()
        return redirect(request.path)

    # MARK ALL AS READ
    if request.method == "POST" and "mark_all_read" in request.POST:
        if request.user.groups.filter(name__in=['Manager', 'Editor']).exists() or request.user.is_superuser:
            notifications = Notification.objects.all()
            for n in notifications:
                n.read_by_admins.add(request.user)
        else:
            request.user.notifications.filter(read=False).update(read=True)
        return redirect(request.path)

    # Load notifications
    page_number = request.GET.get('page', 1)
    if request.user.groups.filter(name__in=['Manager', 'Editor']).exists() or request.user.is_superuser:
        # Managers/Editors: all notifications, except those marked deleted by this user
        user_notifications = Notification.objects.exclude(deleted_by_admins=request.user).order_by('-created_at')
        unread_count = user_notifications.exclude(read_by_admins=request.user).count()
    else:
        # Regular users: only their own
        user_notifications = request.user.notifications.exclude(deleted_by_users=request.user).order_by('-created_at')
        unread_count = user_notifications.filter(read=False).count()

    paginator = Paginator(user_notifications, 10)
    page_obj = paginator.get_page(page_number)
    
    # Check if user is manager/editor
    is_manager_editor = request.user.groups.filter(name__in=['Manager','Editor']).exists() or request.user.is_staff

    

    context = {
        'notifications': page_obj,
        'unread_count': unread_count,
        'is_manager_editor': is_manager_editor,
    }

    template = (
        'dashboardnotification.html'
        if request.resolver_match.url_name == 'dashboardnotification'
        else 'notification.html'
    )
    return render(request, template, context)







@login_required
def delete_comment(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.user != request.user and not request.user.is_superuser:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        comment.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@require_POST
def edit_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({"success": False, "error": "Comment not found"})

    # 🔐 Permission check
    if comment.user != request.user:
        return JsonResponse({"success": False, "error": "Permission denied"})

    new_text = request.POST.get("comment", "").strip()

    if not new_text:
        return JsonResponse({"success": False, "error": "Comment cannot be empty"})

    comment.comment = new_text
    comment.save()

    return JsonResponse({
        "success": True,
        "comment": comment.comment
    })

def search(request):
    keyword = request.GET.get('keyword', '').strip()
    if keyword and len(keyword) >= 2:
        results = Blog.objects.filter(
            Q(title__icontains=keyword) | 
            # Q(short_description__icontains=keyword) | 
            # Q(blog_body__icontains=keyword) |
            Q(author__username__icontains=keyword) |
            Q(category__category_name__icontains=keyword),
            status='Published'
        ).order_by('-created_at')
    else:
        results = Blog.objects.none()
    
    total_results = results.count()

    paginator = Paginator(results, 24)
    page_number = request.GET.get('page', 1)
    blogs_page = paginator.get_page(page_number)

    context = {
        'results': blogs_page,
        'keyword': keyword,
        'min_length_required': len(keyword) < 2 if keyword else False,
        'total_results': total_results,
    }
    return render(request, 'search.html', context)

@login_required
def following_feed(request):
    followed_users = Follow.objects.filter(
        follower=request.user
    ).values_list('following', flat=True)

    blogs = Blog.objects.filter(
        author__in=followed_users,
        status='Published'
    ).order_by('-created_at')

    return render(request, 'blog/following_feed.html', {'blogs': blogs})