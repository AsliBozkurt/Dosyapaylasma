from django.core.exceptions import PermissionDenied

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


def route_permissions(permission):
    """django-rest-framework permission decorator for custom methods"""

    def decorator(drf_custom_method):
        def _decorator(self, *args, **kwargs):
            if self.request.user.has_perm(permission):
                return drf_custom_method(self, *args, **kwargs)
            else:
                raise PermissionDenied()

        return _decorator

    return decorator


class BlocklistPermission(BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):

        ip_addr = get_client_ip(request)

        logger.info(f"Gelen IP : {ip_addr}")

        # blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
        # return blocked
        return


def any_permission_drf_required(user, allowed_perms=[]):
    """
    Kullanıcının yetkilerini kontrol eder
    """

    for perm in allowed_perms:
        if user.has_perm(perm):
            return True

    return False
