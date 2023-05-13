from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.utils.translation import gettext_lazy as _
from filemanager.models import FileStorageSize


@login_required
def home(request):
    user = request.user

    try:
        FileStorageSize.objects.get(user=user)
    except:
        FileStorageSize.objects.create(user=user)

    return render(request, "filemanager/home.html", {"title": _("File Manager")})
