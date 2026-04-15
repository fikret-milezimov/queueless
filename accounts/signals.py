from django.contrib import messages
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver


@receiver(user_logged_out)
def add_logout_message(request, user, **kwargs):
    if request is not None:
        messages.success(request, "Logged out successfully")
