from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("/accounts/login/")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})
