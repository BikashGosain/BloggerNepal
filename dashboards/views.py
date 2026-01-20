from django.shortcuts import get_object_or_404, render, redirect
from blogs.models import Category, Blog
from django.contrib.auth.decorators import permission_required
from .forms import BlogPostForm, CategoryForm, AddUserForm, EditUserForm
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from django.contrib import messages
from django.core.exceptions import PermissionDenied

from django.contrib import messages
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

    return render(request, 'dashboard/dashboard.html', context)


def categories(request):
    return render(request, 'dashboard/categories.html')

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
        'dashboard/add_category.html',
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
        'dashboard/edit_category.html',
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

    # Show all posts if admin/editor/manager, otherwise only own posts
    if user.is_superuser or user.groups.filter(name__in=['Editor', 'Manager']).exists():
        posts = Blog.objects.all()
    else:
        posts = Blog.objects.filter(author=user)

    context = {
        'posts': posts
    }

    return render(request, 'dashboard/posts.html', context)


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
    return render(request, 'dashboard/add_post.html', context)

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
    return render(request, 'dashboard/edit_post.html', context)

def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)

    if not (request.user.is_superuser or request.user.groups.filter(name__in=['Manager']).exists()):
        messages.error(request, "❌ You do not have permission to delete this post.")
        return redirect('posts')
    
    post.delete()
    messages.success(
                request,
                f"✅Post with Title '{post.title}' deleted successfully."
            )
    return redirect('posts')


def users(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'dashboard/users.html', context)


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
        
    return render(request, 'dashboard/add_user.html', context)

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
    return render(request, 'dashboard/edit_user.html', context)

@permission_required('auth.delete_user', raise_exception=True)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, f'Username "{user}" deleted successfully. ✅')
    return redirect('users')