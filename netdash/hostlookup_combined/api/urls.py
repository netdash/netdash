from django.urls import path

from .views import HostView
from ..models import can_view_permission_dispatch

app_name = 'hostlookup-api'

urlpatterns = [
    path('', can_view_permission_dispatch(HostView).as_view(), name='host-lookup'),
]
