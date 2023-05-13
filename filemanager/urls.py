from django.urls import path

from .views import *

app_name = "filemanager"

urlpatterns = [
    path("", home, name="filemanager_home"),
]
