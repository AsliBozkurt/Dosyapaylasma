from django import template

from users.utils import get_gravatar_url

register = template.Library()


@register.simple_tag
def avatar_url(user, size=50, gravatar_only=False):
    """
    A template tag that receives a user and size and return
    the appropriate avatar url for that user.
    Example usage: {% avatar_url request.user 50 %}
    """

    if not gravatar_only and hasattr(user, "userprofile") and user.userprofile.avatar:
        return user.userprofile.avatar.url

    if hasattr(user, "email"):
        gravatar_url = get_gravatar_url(user.email, size=size)
        if gravatar_url is not None:
            return gravatar_url

    return versioned_static_func("assets/img/default-user-avatar.png")
