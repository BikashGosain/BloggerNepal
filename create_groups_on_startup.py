import django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_main.settings')
django.setup()

from django.contrib.auth.models import Group

for group_name in ["Editor", "Manager"]:
    Group.objects.get_or_create(name=group_name)
    print(f"Group '{group_name}' ensured.")
