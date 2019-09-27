from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


def login(request):
    return HttpResponseRedirect(settings.LOGIN_URL)


@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))
