from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save

from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import pytz
import os
import uuid

def upload_avatar_to(instance, filename):
    filename, ext = os.path.splitext(filename)
    return os.path.join(
        "avatar_images",
        "avatar_{uuid}_{filename}{ext}".format(uuid=uuid.uuid4(), filename=filename, ext=ext),
    )



class CustomUser(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="userprofile")
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    timezone = models.CharField(
        verbose_name=_("current time zone"),
        max_length=250,
        choices=[(t, t) for t in pytz.common_timezones],
        help_text=_("Select your current time zone"),
        default="UTC",
    )
    avatar = models.ImageField(
        verbose_name=_("profile picture"),
        upload_to=upload_avatar_to,
        blank=True,
    )
    phone = models.CharField(_("Phone"), max_length=50, blank=True, null=True)
    address = models.CharField(_("Address"), max_length=50, blank=True, null=True)
    city = models.CharField(_("City"), max_length=50, blank=True, null=True)
    country = models.CharField(_("Country"), max_length=50, blank=True, null=True)
    class Meta:
        verbose_name = _("User profile")
        verbose_name_plural = _("User profiles")


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance, site_id=settings.SITE_ID)

    instance.userprofile.save()
