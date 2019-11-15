from django.urls import path

from .views import HostLookupView
from .models import can_view_permission_dispatch

app_name = 'hostlookup'
urlpatterns = [
    path(r'', can_view_permission_dispatch(HostLookupView).as_view(), name='index'),
]
