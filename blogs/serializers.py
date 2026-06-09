from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'short_description',
            'blog_body',
            'views',
            'created_at'
        ]