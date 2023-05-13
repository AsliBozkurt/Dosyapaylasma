from django.urls import path, re_path

from .views import *

app_name = "users"

urlpatterns = [
     path("profile/", profile, name="user_profile"),
]
