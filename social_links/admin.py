from django.contrib import admin
from .models import SocialLinks

# Register your models here.

class SocialLinksAdmin(admin.ModelAdmin):
    list_display = ('platform', 'link', 'created_at', 'updated_at')  # fields to be displayed in admin panel
    search_fields = ('platform', 'link')  # enable searching by platform name or link
    list_filter = ('created_at', 'updated_at')  # filters for date fields

    def is_manager_or_superuser(self, user):
        return user.is_superuser or user.groups.filter(name='Manager').exists()

    # Allow add
    def has_add_permission(self, request):
        return self.is_manager_or_superuser(request.user)

    # Allow change/edit
    def has_change_permission(self, request, obj=None):
        return self.is_manager_or_superuser(request.user)

    # Allow delete
    def has_delete_permission(self, request, obj=None):
        return self.is_manager_or_superuser(request.user)


admin.site.register(SocialLinks, SocialLinksAdmin)