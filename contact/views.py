from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

import threading
from django.core.mail import EmailMessage
from django.urls import reverse

def send_email_async(email):
    email.send(fail_silently=False)

@login_required
def contact_view(request):
    user = request.user  # always get user first

    # Check if user has email before processing POST
    if not user.email:
        messages.info(
            request,
            '⚠️ Your account has no email address. '
            'Please <a href="{}">add your email here</a>.'.format(reverse('edit_profile'))
        )  # send them to edit profile page
        return redirect("home")
    
    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        email = EmailMessage(
            subject=f"{subject}",
            body=f"""
Username: {user.username}
Email: {user.email}
Subject: {subject}
Message:
{message}
""",
            from_email=settings.EMAIL_HOST_USER,
            to=["gosainbikash0@gmail.com"],
            reply_to=[user.email],
        )

        # Send email in a separate thread
        threading.Thread(target=send_email_async, args=(email,)).start()

        # Immediately return response
        messages.success(request, "Message sent successfully!")
        return redirect("home")

    return render(request, "home.html")

