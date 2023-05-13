# users/forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from allauth.account.forms import LoginForm, SignupForm


from users.models import CustomUser, UserProfile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserDetailForm(UserChangeForm):
    password = None
    password1 = None
    password2 = None

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
        )


class CustomLoginForm(LoginForm):
    pass


class CustomSignupForm(SignupForm):
    is_privacy = forms.BooleanField(required=True)

    def signup(self, request, user):
        """Required, or else it throws deprecation warnings"""

        user.save()


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            "timezone",
            "phone",
            "address",
            "city",
            "country",
        )
