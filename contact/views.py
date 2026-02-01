from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.urls import reverse

@login_required
def contact_view(request):
    user = request.user

    # Check if user has email
    if not user.email:
        messages.info(
            request,
            '⚠️ Your account has no email. Add it <a href="{}">here</a>.'.format(
                reverse('edit_profile')
            )
        )
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

        # Send email synchronously with error handling
        try:
            email.send(fail_silently=False)
            messages.success(request, "Message sent successfully!")
        except Exception as e:
            messages.error(request, "Message could not be sent. Check your internet connection.")

        return redirect(next_page)

    return render(request, "contact.html")
