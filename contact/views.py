from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

import threading
from django.core.mail import EmailMessage

def send_email_async(email):
    email.send(fail_silently=False)

@login_required
def contact_view(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        user = request.user

        if not user.email:
            messages.error(request, "Your account has no email address.")
            return redirect("home")

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

