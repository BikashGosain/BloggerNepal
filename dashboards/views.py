from django.shortcuts import get_object_or_404, render, redirect
from blogs.models import Category, Blog, Notification
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.decorators import permission_required

from follow_following.models import Follow
from .forms import BlogPostForm, CategoryForm, AddUserForm, EditUserForm, ProfileEditForm  
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Q

from django.contrib import messages
from django.core.exceptions import PermissionDenied

from django.contrib import messages
from django.http import JsonResponse


from django.urls import reverse # If email is missing, show a clickable link 
# Create your views here.

# def dashboard(request):
#     category_count = Category.objects.all().count()
#     blogs_count = Blog.objects.all().count()

#     context = {
#         'category_count': category_count,
#         'blogs_count': blogs_count,
#     }

#     return render(request, 'dashboard/dashboard.html',context)


def dashboard(request):
    user = request.user

    # Categories count (only self for normal users)
    if user.is_superuser or user.groups.filter(name__in=['Editor','Manager']).exists():
        category_count = Category.objects.all().count()
        blogs_count = Blog.objects.all().count()
    else:
        category_count = Category.objects.filter(author=user).count()
        blogs_count = Blog.objects.filter(author=user).count()

    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
    }

    return render(request, 'dashboard.html', context)


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

    if request.method == 'POST' and form.is_valid():
        category = form.save(commit=False)  # ← don't save yet
        category.author = request.user      # ← set the logged-in user as author
        category.save()                     # ← now save to DB

        messages.success(
            request,
            f"✅ Category '{category.category_name}' added successfully."
        )
        return redirect('categories')

    return render(
        request,
        'add_category.html',
        {'form': form}
    )



def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

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

    return render(
        request,
        'edit_category.html',
        {'form': form, 'category': category}
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



# blog post crud

def posts(request):
    user = request.user
    query = request.GET.get('q', '')  # search keyword
    status_filter = request.GET.get('status', '')  # filter by status

    # Show all posts if admin/editor/manager, otherwise only own posts
    if user.is_superuser or user.groups.filter(name__in=['Editor', 'Manager']).exists():
        posts = Blog.objects.all()
    else:
        posts = Blog.objects.filter(author=user)

    # Filter by search keyword
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(blog_body__icontains=query)
        )

    # Filter by status if provided
    if status_filter:
        posts = posts.filter(status=status_filter)

    context = {
        'posts': posts,
        'query': query,
        'status_filter': status_filter,
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
                "❌ Post was not added. Please fill the blog body too below."
            )
    else:
        form = BlogPostForm()
    context = {
        'form': form,
    }
    return render(request, 'add_post.html', context)

def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
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
                "❌ Post was not added. Please fill the blog body too below."
            )
    form = BlogPostForm(instance=post)
    context = {
        'form': form,
        'post': post,
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
    users = User.objects.all()
    context = {
        'users': users,
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
    user = get_object_or_404(User, pk=pk)
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
    """
    Display logged-in user's profile, followers, following, and posts
    """
    user = request.user

    # 🔹 ACTIVE TAB (default: posts)
    tab = request.GET.get('tab', 'posts')

    # 🔹 SEARCH QUERY
    search = request.GET.get('search', '').strip()

    # 🔹 EMAIL WARNING
    if not user.email:
        messages.info(
            request,
            '⚠️ Your account has no email address. '
            f'Please <a href="{reverse("edit_profile")}">add your email here</a>.'
        )

    # 🔹 POSTS
    posts = Blog.objects.filter(author=user)

    # 🔹 FOLLOWERS
    followers = Follow.objects.filter(following=user).select_related('follower')
    if tab == 'followers' and search:
        followers = followers.filter(follower__username__icontains=search)

    # 🔹 FOLLOWING
    following = Follow.objects.filter(follower=user).select_related('following')
    if tab == 'following' and search:
        following = following.filter(following__username__icontains=search)

    # 🔹 IDs of users current logged-in user is following (for Follow/Unfollow button)
    user_following_ids = list(Follow.objects.filter(
        follower=user
    ).values_list('following_id', flat=True))

    context = {
        'user': user,
        'tab': tab,
        'search': search,

        'posts': posts,
        'followers': followers,
        'following': following,

        'my_followers_count': followers.count(),
        'my_following_count': following.count(),
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

    # Base queryset
    followers = Follow.objects.filter(
        following=user_obj
    ).select_related('follower')

    # Handle search
    search_query = request.GET.get('search', '').strip()
    if search_query:
        followers = followers.filter(
            follower__username__icontains=search_query
        )

    # IDs of users current logged-in user is following
    user_following_ids = []
    if request.user.is_authenticated:
        user_following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)

    return render(request, 'dashboardfollowers_list.html', {
        'user_obj': user_obj,
        'followers': followers,
        'user_following_ids': list(user_following_ids),
    })

# FOLLOWING LIST
def dashboardfollowing_list(request, username):
    user_obj = get_object_or_404(User, username=username)

    following = Follow.objects.filter(
        follower=user_obj
    ).select_related('following')
    # Handle search
    search_query = request.GET.get('search', '').strip()
    if search_query:
        following = following.filter(
            follower__username__icontains=search_query
        )

    # IDs of users current logged-in user is following
    user_following_ids = []
    if request.user.is_authenticated:
        user_following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)

    return render(request, 'dashboardfollowing_list.html', {
        'user_obj': user_obj,
        'following': following,
        'user_following_ids': list(user_following_ids),
    })