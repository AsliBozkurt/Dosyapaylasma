from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from django.utils.translation import gettext_lazy as _

from users.forms import ProfileForm, UserForm
from users.models import CustomUser, UserProfile


@login_required
def profile(request):
    user = request.user

    title = _("My profile")

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, _("Successfully Saved"))
            return redirect("users:user_profile")
        else:
            messages.error(request, _("Please correct the wrong places"))
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.userprofile)
    return render(
        request,
        "users/profile_update_form.html",
        {"user_form": user_form, "profile_form": profile_form, "title": title},
    )
