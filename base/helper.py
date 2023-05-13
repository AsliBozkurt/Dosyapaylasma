from users.models import CustomUser


def login_as(request):
    """Dikkat sadece request gönderiniz.
    login_as(request)

    Bu fonksiyonun daha iyi iş yapabilmesi için,
    newtork üzerinden IP kısıtlaması getirilmelidir.

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.session.get("pinar") == None:
        return request.user

    # super user mıyız.
    if not request.user.is_superuser:
        return request.user

    user = CustomUser.objects.get(pk=request.session.get("pinar"))

    return user
