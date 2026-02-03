from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from blogs.models import Blog, Category
from django.contrib.auth.models import User, Group
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
    blog_body = forms.CharField(widget=CKEditorUploadingWidget(), required=False)  # CKEditor only

    class Meta:
        model = Blog
        fields = ('title', 'category', 'featured_image', 'short_description', 'blog_body', 'status', 'is_featured')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['featured_image'].required = False

class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email', 'is_active',
            'is_staff', 'is_superuser', 'groups', 'user_permissions'
        )

    def __init__(self, *args, **kwargs):
        # Pop the logged-in user from kwargs
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)

        # Remove all default help texts
        for field in self.fields.values():
            field.help_text = None

        # Role-based field access
        if self.request_user and not self.request_user.is_superuser:
            # For Manager
            allowed_fields = ['first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'groups', 'password1', 'password2']
            for field_name in list(self.fields):
                if field_name not in allowed_fields:
                    self.fields.pop(field_name)

            # Limit groups to "Editor" only
            if 'groups' in self.fields:
                self.fields['groups'].queryset = Group.objects.filter(name='Editor')

    # Validate unique email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = None

        
        # Role-based field access
        if self.request_user and not self.request_user.is_superuser:
            allowed_fields = ['first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'groups']
            for field_name in list(self.fields):
                if field_name not in allowed_fields:
                    self.fields.pop(field_name)

            # Limit groups to "Editor" only
            if 'groups' in self.fields:
                self.fields['groups'].queryset = Group.objects.filter(name='Editor')

    # Validate unique username and email while allowing current user's values
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        # Optional: remove help texts
        for field in self.fields.values():
            field.help_text = None
