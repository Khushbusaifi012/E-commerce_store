from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label="Your name",
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")
