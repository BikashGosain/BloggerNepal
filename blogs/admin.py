from django.contrib import admin
from .models import Category, Blog, Comment
from django.db.models import Count

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'blog_count')
    search_fields = ('category_name',)
    list_filter = ('created_at', 'updated_at', 'author')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Annotate each category with the number of blogs
        qs = qs.annotate(blog_count=Count('blog'))
        return qs

    def blog_count(self, obj):
        return obj.blog_count
    blog_count.admin_order_field = 'blog_count'  # allows sorting by blog count
    blog_count.short_description = 'Number of Blogs'


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}  # auto fill slug field from title field
    list_display = ('title', 'author', 'category', 'status', 'is_featured', 'created_at')  # fields to be displayed in admin panel
    search_fields = ( 'id', 'title', 'category__category_name', 'status')  # search by title and author's username
    list_editable = ('is_featured', 'status', 'category')  # make is_featured and status editable in list display
    list_filter = ('category', 'status', 'created_at', 'updated_at', 'author', 'updated_at')  # filter by category, status, created_at and author

class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'comment', 'created_at')
    search_fields = ('blog__title', 'user__username', 'comment')
    list_filter = ('created_at', 'updated_at', 'user')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)