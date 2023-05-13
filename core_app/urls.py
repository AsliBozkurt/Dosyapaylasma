from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

admin.site.site_header = "Super User"


urlpatterns = [
    re_path("api/(?P<version>(v1))/", include("api.urls")),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    # rest-auth
    re_path("api/rest-auth/", include("rest_auth.urls")),
    re_path("api/rest-auth/registration/", include("rest_auth.registration.urls")),
    # Admin panel
    path("aurora/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("home.urls")),
    path("users/", include("users.urls")),
    path("file-manager/", include("filemanager.urls")),
]
