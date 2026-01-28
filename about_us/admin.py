from django.contrib import admin
from .models import AboutUs

# Register your models here.
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'updated_at')  # fields to display in admin list
    search_fields = ('question', 'answer')  # enable searching by question or answer
    list_filter = ('created_at', 'updated_at')  # filter by date created/updated

    # def has_add_permission(self, request):
    #     count = AboutUs.objects.all().count()
    #     if count == 0:
    #         return True
    #     else:
    #         return False
    
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

admin.site.register(AboutUs, AboutUsAdmin)