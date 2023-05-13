from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from core_app.storage_backends import PrivateMediaStorage
from users.models import CustomUser

WEEK_NUMBER = datetime.today().isocalendar()[1]
YEAR = datetime.today().year


def user_directory_path(instance, filename):
    """Django
    https://docs.djangoproject.com/en/dev/ref/models/fields/#filefield

    Args:
        instance ([obj]): []
        filename ([string]): []

    Returns:
        [type]: [string]
    """

    return "user_file/{0}/{1}/{2}/{3}".format(instance.user.id, YEAR, WEEK_NUMBER, filename)


class FileStorageSize(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    size = models.BigIntegerField(default=10485760, help_text=_("Byte"))


class FileManager(models.Model):
    STORAGE_TYPE_CHOOSE = [
        ("public", _("Public")),
        ("private", _("Private")),
    ]

    user = models.ForeignKey(CustomUser, related_name="filemanager", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    file_public = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    file_private = models.FileField(
        storage=PrivateMediaStorage(), upload_to=user_directory_path, blank=True, null=True
    )
    storage_type = models.CharField(
        max_length=20,
        choices=STORAGE_TYPE_CHOOSE,
        default="public",
        verbose_name=_("Upload File Type"),
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True)
