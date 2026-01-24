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
    user = request.user

    if not user.email:
        messages.info(request, '⚠️ Your account has no email. Add it <a href="{}">here</a>.'.format(reverse('edit_profile')))
        return redirect('home')

    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        next_page = request.POST.get("next", "/")  # redirect back to page submitted from

        email = EmailMessage(
            subject=subject,
            body=f"Username: {user.username}\nEmail: {user.email}\nSubject: {subject}\nMessage:\n{message}",
            from_email=settings.EMAIL_HOST_USER,
            to=["gosainbikash0@gmail.com"],
            reply_to=[user.email],
        )

        threading.Thread(target=send_email_async, args=(email,)).start()
        messages.success(request, "Message sent successfully!")
        return redirect(next_page)

    return render(request, "contact.html")


