import json

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from blogs.models import Blog, Category


class Command(BaseCommand):
    help = "Load blog dataset"

    def handle(self, *args, **kwargs):

        with open('blogs_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        user = User.objects.first()

        for item in data:

            category, created = Category.objects.get_or_create(
                category_name=item['category']
            )

            Blog.objects.create(
                title=item['title'],
                category=category,
                author=user,
                short_description=item['short_description'],
                blog_body=item['blog_body'],
                status='Published'
            )

        self.stdout.write(
            self.style.SUCCESS('Blogs imported successfully')
        )