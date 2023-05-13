from django.urls import include, path, re_path

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import base, users, filemanager

app_name = "api"

urlpatterns = [
    path("hello/", base.HelloView.as_view()),
    path("hello2/", base.HelloAView.as_view()),
    # File Manager
    path("file-manager", filemanager.FileManagerView.as_view()),
    path("file-manager/<int:pk>", filemanager.FileManagerDetail.as_view()),
    path("file-manager-filter/", filemanager.FileManagerFilter.as_view()),
    path("file-manager-size/", filemanager.FileManagerSizeView.as_view()),
    # users
    path("users", users.UserList.as_view()),
    path("users/users-profile-avatar", users.UsersProfileAvatarDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=["json"])
