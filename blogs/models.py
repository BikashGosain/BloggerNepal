from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name
    


# status may be draft or published so we made dropdown
STATUS_CHOICES = (
    # (0, 'Draft'),
    # (1, 'Published'),
    ('Draft', 'Draft'),
    ('Published', 'Published'),
)

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # on delete category all posts related category will be deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE) # on delete user all posts related user will be deleted
    featured_image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=False, null=False)
    short_description = models.TextField(max_length=200)
    # blog_body = models.TextField(max_length=5000)
    # blog_body = HTMLField()
    blog_body = RichTextUploadingField()
    status = models.CharField(max_length=20, default='Draft', choices=STATUS_CHOICES)  # draft = 0, published = 1 status may be draft or published so we made dropdown
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # on delete user all comments related user will be deleted
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE) # on delete blog all comments related blog will be deleted
    comment = models.TextField(max_length=250)

    # for reply button in each comments

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment