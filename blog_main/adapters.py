from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.contrib import messages
from allauth.exceptions import ImmediateHttpResponse

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            user = sociallogin.user
            if not user.is_active:
                messages.error(request, 'Your account has been deactivated. Please contact support.')
                raise ImmediateHttpResponse(redirect('/'))