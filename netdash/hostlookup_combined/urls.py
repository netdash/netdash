from django.conf.urls import url

from .views import HostLookupView
from .models import can_view_permission_dispatch


app_name = 'hostlookup'
urlpatterns = [
    url(r'^$', can_view_permission_dispatch(HostLookupView).as_view(), name='index'),
]
