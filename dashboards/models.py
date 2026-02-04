from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='created_users',
        help_text="The user who created this account"
    )
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return None
    
    def get_creator_display(self):
        """Return the creator's username or 'Self' if user created their own account"""
        if self.created_by:
            return self.created_by.username
        return "Self"

# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)