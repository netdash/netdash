from django.conf.urls import url

from .views import HostLookupView
from .models import can_view_permission


app_name = 'hostlookup'
urlpatterns = [
    url(r'^$', can_view_permission(HostLookupView.as_view()), name='index'),
]
