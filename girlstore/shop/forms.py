from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    """Login with username or the email stored on the account."""

    def clean(self):
        username_or_email = (self.cleaned_data.get('username') or '').strip()
        password = self.cleaned_data.get('password')
        if not username_or_email or not password:
            raise self.get_invalid_login_error()

        user = authenticate(self.request, username=username_or_email, password=password)
        if user is None:
            match = User.objects.filter(email__iexact=username_or_email).first()
            if match:
                user = authenticate(self.request, username=match.username, password=password)

        if user is None:
            raise self.get_invalid_login_error()

        self.user_cache = user
        self.confirm_login_allowed(user)
        return self.cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
