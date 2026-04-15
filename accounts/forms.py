from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = ""

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "password1", "password2")
