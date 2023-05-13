import json

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from users.models import CustomUser
from allauth.account.admin import EmailAddress


def site(request):

    return {
        "site_logo": settings.SITE_LOGO,
    }

def resolver_context_processor(request):
    return {
        "app_name": request.resolver_match.app_name,
        "namespace": request.resolver_match.namespace,
        "url_name": request.resolver_match.url_name,
    }



def login_as(request):
    """Lüften base.helper.login_as bakınız

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    # session var mı?
    if request.session.get("pinar") == None:
        return {"login_as": False, "login_as_username": request.user.username}

    # super user mıyız.
    # if not request.user.is_superuser:
    #    return {'login_as': False,  'login_as_username' : request.user.username}

    a = CustomUser.objects.get(pk=request.session.get("pinar"))

    return {
        "login_as": True,
        "login_as_username": a.username,
        "login_as_email": a.email,
        "login_as_id": a.id,
        "login_as_site": a.bahar_userprofile.site,
    }
