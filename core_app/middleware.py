from django.http import HttpResponseForbidden


from django.utils.deprecation import MiddlewareMixin


class UserCheckSuperckMiddleware(MiddlewareMixin):
    """
    SuperUser in site=1 harici girişi yasaktır.
    """

    def process_request(self, request):

        if request.user.is_authenticated and request.user.is_superuser:
            if request.user.bahar_userprofile.site.pk != 1:
                return HttpResponseForbidden("Forbidden")
        return
