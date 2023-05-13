from django.contrib.auth import get_user_model

from allauth.account.models import EmailAddress
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from users.models import CustomUser, UserProfile

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.utils import email_address_exists, get_username_max_length
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("pk", "first_name", "last_name")


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    class Meta:
        model = CustomUser
        fields = ("pk", "username", "email", "first_name", "last_name")
        read_only_fields = ("email",)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    is_verified = serializers.SerializerMethodField()

    def get_is_verified(self, user):
        return user.emailaddress_set.filter(verified=1).count() > 0

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "is_verified")

    def update(self, instance, validated_data):
        new_email = validated_data.pop("email", None)
        user = super(CustomUserDetailsSerializer, self).update(instance, validated_data)

        # http://stackoverflow.com/questions/19755102/django-allauth-change-user-email-with-without-verification
        if new_email:
            context = self.context
            request = context.get("request", None)
            if request:
                EmailAddress.objects.add_email(request, user, new_email, confirm=True)

        return user


class CustomRegisterUserSerializer(RegisterSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def custom_signup(self, request, user):
        pass

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])

        # get_cleaned_data
        # https://github.com/Tivix/django-rest-auth/blob/3c36004c44855cd25b535fe822b16d9e3fa1a3d1/rest_auth/registration/serializers.py#L199
        CustomUser.objects.filter(id=user.id).update()

        return user


class UserProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("avatar",)
