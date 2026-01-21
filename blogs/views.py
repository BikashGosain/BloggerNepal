from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Blog, Category, Comment
from django.db.models import Q

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
        'user' : user
    }
    return render(request, 'blogs.html', context)


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