from django.contrib.sites.models import Site
from django.shortcuts import Http404, get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    DjangoModelPermissions,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser, UserProfile
from users.serializers import UserProfileAvatarSerializer, UserMiniSerializer

from users.utils import get_gravatar_url
from django.db.models import Q


def avatar_url(user, size=50, gravatar_only=False):
    """
    A template tag that receives a user and size and return
    the appropriate avatar url for that user.
    Example usage: {% avatar_url request.user 50 %}
    """

    if not gravatar_only and hasattr(user, "bahar_userprofile") and user.bahar_userprofile.avatar:
        return user.bahar_userprofile.avatar.url

    if hasattr(user, "email"):
        gravatar_url = get_gravatar_url(user.email, size=size)
        if gravatar_url is not None:
            return gravatar_url

    return versioned_static_func("assets/img/default-user-avatar.png")


class UsersProfileAvatarDetail(APIView):
    def get_object(self, user):
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, version, format=None):
        user = self.request.user
        snippet = self.get_object(user)

        if snippet.avatar == "":
            avatar_url_str = avatar_url(user, 100)
            return Response({"avatar": avatar_url_str})

        serializer = UserProfileAvatarSerializer(snippet)
        return Response(serializer.data)

    def patch(self, request, version, format=None):
        user = self.request.user
        snippet = self.get_object(user)
        serializer = UserProfileAvatarSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, version, format=None):
        user = self.request.user
        snippet = self.get_object(user)

        snippet.avatar = None
        snippet.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(APIView):
    """
    UserList
    """

    def get(self, request, version, format=None):
        snippets = CustomUser.objects.filter(~Q(id=1))
        serializer = UserMiniSerializer(snippets, many=True)
        return Response(serializer.data)
