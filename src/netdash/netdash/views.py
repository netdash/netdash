from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))
