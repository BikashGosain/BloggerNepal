from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from follow_following.models import Follow
from .models import Blog, Category, Comment, Notification, Report
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

def posts_by_category(request, category_id):
    # Logic to fetch posts by category_id
    posts = Blog.objects.filter(category=category_id, status='Published')
    # for check it category exists if not redirect to home

    try:
        category = Category.objects.get(id=category_id)
    except:
        return redirect('home')

    # # (remember to create 404.html page for 404 error but for 5050 error create errorcode.html)for get object or 404 error page if category not found
    # # for this to apply and show 404error.html page made changes in settings.py file debug = False and allowed host = ['*']
    # category = get_object_or_404(Category, id=category_id)

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'posts_by_category.html', context)


def blogs(request, slug):
    user = request.user
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')

    # 🔔 MARK NOTIFICATION AS READ (if coming from notification)
    notification_id = request.GET.get("notification")
    if request.user.is_authenticated and notification_id:
        request.user.notifications.filter(
            id=notification_id,
            blog=single_blog
        ).update(read=True)

    # Increment view count
    single_blog.views += 1
    single_blog.save(update_fields=['views'])

    is_following = False
    if request.user.is_authenticated and request.user != single_blog.author:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=single_blog.author
        ).exists()

    user_reported = (
        single_blog.reports.filter(user=request.user).exists()
        if request.user.is_authenticated else False
    )

    unread_count = (
        request.user.notifications.filter(read=False).count()
        if request.user.is_authenticated else 0
    )

    if request.method == 'POST':
        text = request.POST.get('comment', '').strip()
        parent_id = request.POST.get('parent_id')

        if text:
            comment = Comment(
                blog=single_blog,
                user=request.user,
                comment=text
            )
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
        'unread_count': unread_count,
        'is_following': is_following,
    }
    return render(request, 'blogs.html', context)

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

    # Check if already reported
    if blog.reports.filter(user=user).exists():
        messages.info(request, "You have already reported this blog.")
        return redirect(blog.get_absolute_url())

    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        # Create report
        Report.objects.create(blog=blog, user=user, reason=reason if reason else None)

        # Create notification for blog owner
        if reason:
            message = f"Your blog '{blog.title}' has been reported.Reason: {reason}"
        else:
            message = f"Your blog '{blog.title}' has been reported."
        Notification.objects.create(user=blog.author, blog=blog, message=message)

        messages.success(request, "Report submitted.")
        return redirect(blog.get_absolute_url())




@login_required
def notifications(request):

    # Handle delete single notification
    if request.method == "POST" and "delete_one" in request.POST:
        notification_id = request.POST.get("delete_one")
        request.user.notifications.filter(id=notification_id).delete()
        return redirect(request.path)
    
    # Handle delete all notifications
    if request.method == "POST" and "delete_all" in request.POST:
        request.user.notifications.all().delete()
        return redirect(request.path)
    
    # 🔔 MARK SINGLE NOTIFICATION AS READ
    if request.method == "POST" and "mark_read" in request.POST:
        notification_id = request.POST.get("mark_read")
        request.user.notifications.filter(id=notification_id).update(read=True)
        return redirect(request.path)
    
    # 🔔 MARK ALL AS READ
    if request.method == "POST" and "mark_all_read" in request.POST:
        notification_id = request.POST.get("mark_read")
        request.user.notifications.filter(read=False).update(read=True)
        return redirect(request.path)

    # Load notifications based on user group
    if request.user.groups.filter(name__in=['Admin', 'Manager', 'Editor']).exists() or request.user.is_superuser:
        # Allowed groups see all notifications
        user_notifications = Notification.objects.all().order_by('-created_at')
    else:
        # Other users see only their own notifications
        user_notifications = request.user.notifications.all().order_by('-created_at')

    context = {
        'notifications': user_notifications,
        'unread_count': request.user.notifications.filter(read=False).count(),
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
    keyword = request.GET.get('keyword')
    results = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='Published')
    context = {
        'results': results,
        'keyword': keyword,
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