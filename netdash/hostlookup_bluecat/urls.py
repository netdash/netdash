from django.urls import path

from .views import HostLookupView
from .models import can_view_permission

app_name = 'hostlookup'
urlpatterns = [
    path(r'', can_view_permission(HostLookupView.as_view()), name='index'),
]
