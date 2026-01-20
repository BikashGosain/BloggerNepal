from django import forms
from blogs.models import Blog, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)
    
    # to show exact error in edit catagory field when try to edited to already exixted category: f"Category '{category_name}' already exists."
    # also show error in addnew category too: f"Category '{category_name}' already exists."

    def clean_category_name(self):
        category_name = self.cleaned_data.get('category_name')

        qs = Category.objects.filter(category_name__iexact=category_name)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                f"Category '{category_name}' already exists."
            )

        return category_name
        

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'category', 'featured_image', 'short_description', 'blog_body', 'status', 'is_featured')

class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')