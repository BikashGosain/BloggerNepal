from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

from inymce.django.template.defaultfilters import slugify


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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog')
    author = models.ForeignKey(User, on_delete=models.CASCADE) # on delete user all posts related user will be deleted
    featured_image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=False, null=False)
    short_description = models.TextField(max_length=200)
    # blog_body = models.TextField(max_length=5000)
    # blog_body = HTMLField()
    blog_body = RichTextUploadingField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Draft', choices=STATUS_CHOICES)  # draft = 0, published = 1 status may be draft or published so we made dropdown
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # View tracking
    views = models.PositiveIntegerField(default=0)
    # for like and dislike
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='blog_dislikes', blank=True)

    def get_category_url(self):
        if self.category:
            return reverse('posts_by_category', kwargs={'category_id': self.category.id})
        else:
            return reverse('posts_by_category', kwargs={'category_id': 0})

    def get_category_name(self):
        return self.category.category_name if self.category else "Uncategorized"

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()
    # up to here for like and dislike

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blogs', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title[:1].upper() + self.title[1:]

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


    
# report option on blog
class Report(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user} on {self.blog.title}"
    
    
class Notification(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    # Track which admins/managers/editors have deleted this notification
    deleted_by_admins = models.ManyToManyField(User, blank=True, related_name='deleted_notifications_admin')
    read_by_admins = models.ManyToManyField(User, blank=True, related_name='read_notifications_admin')

    # Track which normal users have deleted this notification
    deleted_by_users = models.ManyToManyField(User, blank=True, related_name='deleted_notifications_user')

    def __str__(self):
        return f"{self.message[:50]} - {self.user.username}"


    

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