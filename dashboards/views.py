# Django shortcuts & utilities
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse # If email is missing, show a clickable link 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify

# Django ORM & utilities
from django.db.models import Q, Count
from django.db.models.functions import ExtractMonth
from calendar import month_name

# Third-party editors
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Local apps & utilities
from blogs.models import Blog, Category, Notification
from .forms import BlogPostForm, CategoryForm, AddUserForm, EditUserForm, ProfileEditForm
from .utils import dashboard_header_context
from follow_following.models import Follow

from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from calendar import month_name
from blogs.models import Blog

# Create your views here.



# def dashboard(request):
#     category_count = Category.objects.all().count()
#     blogs_count = Blog.objects.all().count()

#     context = {
#         'category_count': category_count,
#         'blogs_count': blogs_count,
#     }

#     return render(request, 'dashboard/dashboard.html',context)
# blogs/views.py

def dashboard(request):
    context = dashboard_header_context(request.user)
    return render(request, 'dashboard.html', context)


from django.db.models import Count, Q
from django.shortcuts import render
from blogs.models import Blog, Category

def posts_per_category(request):
    user = request.user

    is_manager = user.groups.filter(name='Manager').exists()
    can_see_all = is_manager or user.is_superuser

    # Counts
    category_count = Category.objects.count()
    blogs_count = Blog.objects.count() if can_see_all else Blog.objects.filter(author=user).count()
    self_posts_count = Blog.objects.filter(author=user).count()

    # All posts per category
    all_posts = Category.objects.annotate(
        count=Count('blog')
    ).values('category_name', 'count')

    # Count Uncategorized for all posts
    uncategorized_count_all = Blog.objects.filter(category__isnull=True).count()
    all_posts = list(all_posts)  # convert to list so we can append
    if uncategorized_count_all > 0:
        all_posts.append({'category_name': 'Uncategorized', 'count': uncategorized_count_all})

    # My posts per category
    my_posts = Category.objects.annotate(
        count=Count('blog', filter=Q(blog__author=user))
    ).values('category_name', 'count')

    # Count Uncategorized for my posts
    uncategorized_count_my = Blog.objects.filter(category__isnull=True, author=user).count()
    my_posts = list(my_posts)
    if uncategorized_count_my > 0:
        my_posts.append({'category_name': 'Uncategorized', 'count': uncategorized_count_my})

    context = {
        'can_see_all': can_see_all,
        'category_count': category_count,
        'blogs_count': blogs_count,
        'self_posts_count': self_posts_count,
        'all_posts_per_category': all_posts,
        'my_posts_per_category': my_posts,
    }

    return render(request, 'analytics/posts_per_category.html', context)



def posts_per_month(request):
    user = request.user

    is_manager = user.groups.filter(name='Manager').exists()
    can_see_all = is_manager or user.is_superuser

    blogs_count = Blog.objects.count() if can_see_all else Blog.objects.filter(author=user).count()
    self_posts_count = Blog.objects.filter(author=user).count()

    all_posts = (
        Blog.objects
        .annotate(month=ExtractMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    my_posts = (
        Blog.objects.filter(author=user)
        .annotate(month=ExtractMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    context = {
        'can_see_all': can_see_all,
        'blogs_count': blogs_count,
        'self_posts_count': self_posts_count,
        'all_posts_per_month': all_posts,
        'my_posts_per_month': my_posts,
        'month_name': month_name,
    }

    return render(request, 'analytics/posts_per_month.html', context)







def categories(request):
    return render(request, 'categories.html')

# def add_category(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('categories')
#     form = CategoryForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'dashboard/add_category.html', context)

def add_category(request):
    form = CategoryForm(request.POST or None)
    allowed_roles = ['Editor', 'Manager']
    can_add = request.user.is_superuser or request.user.groups.filter(name__in=allowed_roles).exists()
    
    if not can_add:
        raise PermissionDenied
        # now no need to show messages.error and return redirect direct 403.html page triger due to raise PermissionDenied
        # messages.error(request, "You are not allowed to add a category.")
        # return redirect('categories')

    if request.method == 'POST' and form.is_valid():
        category = form.save(commit=False)  # ← don't save yet
        category.author = request.user      # ← set the logged-in user as author
        category.save()                     # ← now save to DB

        messages.success(
            request,
            f"✅ Category '{category.category_name}' added successfully."
        )
        return redirect('categories')

    context = {
        'form': form,
        'can_add': can_add,
    }

    return render(
        request,
        'add_category.html',
        context
    )



def edit_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        messages.error(request, f"No category found with ID {pk}.")
        return redirect('categories')
    
    can_edit = request.user == category.author \
               or request.user.groups.filter(name='Manager').exists() \
               or request.user.is_superuser
    if not can_edit:
        messages.error(request, "You are not allowed to edit this category.")
        return redirect('categories')

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()  # Author remains the same
            messages.success(
                request,
                f"✅ Category edited to '{category.category_name}' successfully."
            )
            return redirect('categories')
        
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'can_edit': can_edit,
    }

    return render(
        request,
        'edit_category.html', context
    )





def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # Only allow superuser or users in Editor/Manager groups
    if not (request.user.is_superuser or request.user.groups.filter(name__in=['Manager']).exists()):
        messages.error(request, "❌ You do not have permission to delete this category.")
        return redirect('categories')  # redirect to safe page

    category.delete()
    messages.success(request, f"✅ Category '{category.category_name}' deleted successfully.")
    return redirect('categories')



def posts(request):
    user = request.user

    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')
    featured = request.GET.get('featured', '')
    category_id = request.GET.get('category', '')
    page_number = request.GET.get('page', 1)

    # 🔐 Role-based access
    if user.is_superuser or user.groups.filter(name__in=['Editor', 'Manager']).exists():
        posts_qs = Blog.objects.select_related('author', 'category').all()
    else:
        posts_qs = Blog.objects.select_related('author', 'category').filter(author=user)

    # 🔍 Search: title, category, author
    if query:
        posts_qs = posts_qs.filter(
            Q(title__icontains=query) |
            Q(category__category_name__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        )

    # 🏷 Status filter (Draft / Published)
    if status_filter in ['Draft', 'Published']:
        posts_qs = posts_qs.filter(status=status_filter)

    # ⭐ Featured filter
    if featured == '1':
        posts_qs = posts_qs.filter(is_featured=True)

    # 📂 Category filter
    if category_id:
        posts_qs = posts_qs.filter(category_id=category_id)

    # 📄 Pagination
    paginator = Paginator(posts_qs.order_by('-created_at'), 5)
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'query': query,
        'status_filter': status_filter,
        'featured': featured,
        'category_id': category_id,
        'categories': Category.objects.all(),
    }

    return render(request, 'posts.html', context)



def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # temporarily saving the form
            post.author = request.user  # setting the author
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + "-" + str(post.id)  # generating slug from title
            post.save()  # saving again to update the slug
            messages.success(
                request,
                f"✅ New Post title '{post.title}' added successfully."
            )
            return redirect('posts')
        else:
            messages.error(
                request,
                f"✅ Post edited successfully. New title: '{post.title}' successfully."
            )
    else:
        form = BlogPostForm()
    context = {
        'form': form,
    }
    return render(request, 'add_post.html', context)

def edit_post(request, pk):
    post = Blog.objects.filter(pk=pk).first()
    if not post:
        messages.warning(request, "The post you are trying to edit does not exist.")
        return redirect('posts')
    
    
    allowed_roles = ['Editor', 'Manager']

    can_edit = (
    request.user == post.author
    or request.user.is_superuser
    or request.user.groups.filter(name__in=allowed_roles).exists()
)

    if not can_edit:
        messages.error(request, "You are not allowed to edit this post.")
        return redirect('posts')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + "-" + str(post.id)  # updating slug from title
            post.save()  # saving again to update the slug
            messages.success(
                request,
                f"✅Post edited to this Title '{post.title}' successfully."
            )
            return redirect('posts')
        else:
            messages.error(
                request,
                f"✅ Post not edited for title: '{post.title}'."
            )
    form = BlogPostForm(instance=post)
    context = {
        'form': form,
        'post': post,
        'can_edit': can_edit,
    }
    return render(request, 'edit_post.html', context)

def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    user = request.user

    # Superuser or Manager can delete any post
    if user.is_superuser or user.groups.filter(name__in=['Manager']).exists():
        post.delete()
        messages.success(request, f"✅ Post '{post.title}' deleted successfully.")
        return redirect('posts')

    # Editors and normal users can delete ONLY their own post
    elif post.author == user:
        post.delete()
        messages.success(request, f"✅ Your post '{post.title}' deleted successfully.")
        return redirect('posts')

    # Anyone else cannot delete
    else:
        messages.error(request, "❌ You do not have permission to delete this post.")
        return redirect('posts')
    return redirect('posts')


def users(request):
    page_number = request.GET.get('page', 1)
    users_list = User.objects.all().order_by('username')
    paginator = Paginator(users_list, 2)
    page_obj = paginator.get_page(page_number)
    context = {
        'users': page_obj,
    }
    return render(request, 'users.html', context)


def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # capture created user
            messages.success(
                request,
                f'User "{user.username}" added successfully ✅'
            )
            return redirect('users')
        else:
            messages.error(
                request,
                "User could not be added. Please fix the errors below ❌"
            )
    form = AddUserForm()
    context = {
        'form': form,
    }
        
    return render(request, 'add_user.html', context)

def edit_user(request, pk):
    user = User.objects.filter(pk=pk).first()
    if not user:
        messages.warning(request, "The user you are trying to edit does not exist.")
        return redirect('users')
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Username "{user}" updated successfully. ✅')
            return redirect('users')
    else:
        form = EditUserForm(instance=user)
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'edit_user.html', context)

@permission_required('auth.delete_user', raise_exception=True)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, f'Username "{user}" deleted successfully. ✅')
    return redirect('users')

def profile(request):
    user = request.user

    # Active tab
    tab = request.GET.get('tab', 'posts')
    search = request.GET.get('search', '').strip()
    page_number = request.GET.get('page')

    # Email warning
    if not user.email:
        messages.info(
            request,
            '⚠️ Your account has no email address. '
            f'Please <a href="{reverse("edit_profile")}">add your email here</a>.'
        )

    # 🔹 POSTS (paginated + searchable)
    posts_qs = Blog.objects.filter(author=user).order_by('-created_at')

    if tab == 'posts' and search:
        posts_qs = posts_qs.filter(
            Q(title__icontains=search) |
            Q(short_description__icontains=search) |
            Q(blog_body__icontains=search) |
            Q(author__username__icontains=search) |
            Q(category__category_name__icontains=search)
        )

    posts_qs = posts_qs.order_by('-created_at')
    posts = Paginator(posts_qs, 2).get_page(page_number) if tab == 'posts' else None

    # 🔹 FOLLOWERS (paginated + searchable)
    followers_qs = Follow.objects.filter(
        following=user
    ).select_related('follower')

    if tab == 'followers' and search:
        followers_qs = followers_qs.filter(
            follower__username__icontains=search
        )

    followers = None
    if tab == 'followers':
        followers = Paginator(followers_qs, 2).get_page(page_number)

    # 🔹 FOLLOWING (paginated + searchable)
    following_qs = Follow.objects.filter(
        follower=user
    ).select_related('following')

    if tab == 'following' and search:
        following_qs = following_qs.filter(
            following__username__icontains=search
        )

    following = None
    if tab == 'following':
        following = Paginator(following_qs, 2).get_page(page_number)

    # 🔹 Counts (ALWAYS global, NEVER filtered)
    my_followers_count = Follow.objects.filter(following=user).count()
    my_following_count = Follow.objects.filter(follower=user).count()

    # 🔹 IDs for Follow/Unfollow buttons
    user_following_ids = list(
        Follow.objects.filter(follower=user)
        .values_list('following_id', flat=True)
    )

    context = {
        'user': user,
        'tab': tab,
        'search': search,

        'posts': posts,
        'followers': followers,
        'following': following,

        'my_followers_count': my_followers_count,
        'my_following_count': my_following_count,
        'user_following_ids': user_following_ids,
    }

    return render(request, 'profile.html', context)






def edit_profile(request):
    """
    Edit logged-in user's profile
    """
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Your profile has been updated successfully.")
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'edit_profile.html', context)




def dashboardfollowers_list(request, username):
    user_obj = get_object_or_404(User, username=username)

    followers_qs = Follow.objects.filter(
        following=user_obj
    ).select_related('follower')

    search_query = request.GET.get('search', '').strip()
    if search_query:
        followers_qs  = followers_qs .filter(
            follower__username__icontains=search_query
        )

         # 🔹 Pagination (10 followers per page)
    paginator = Paginator(followers_qs, 2)
    page_number = request.GET.get('page', 1)
    followers = paginator.get_page(page_number)

    return render(request, 'dashboardfollowers_list.html', {
        'user_obj': user_obj,
        'followers': followers,
        'search': search_query,
    })


# FOLLOWING LIST
def dashboardfollowing_list(request, username):
    user_obj = get_object_or_404(User, username=username)

    following_qs = Follow.objects.filter(
        follower=user_obj
    ).select_related('following')

    search_query = request.GET.get('search', '').strip()
    if search_query:
        following_qs = following_qs.filter(
            following__username__icontains=search_query
        )

        # 🔹 Pagination (10 per page)
    paginator = Paginator(following_qs, 2)
    page_number = request.GET.get('page', 1)
    following = paginator.get_page(page_number)

    return render(request, 'dashboardfollowing_list.html', {
        'user_obj': user_obj,
        'following': following,
        'search': search_query,
    })
