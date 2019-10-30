from django.conf.urls import url

from .views import HostLookupView


app_name = 'hostlookup'
urlpatterns = [
    url(r'^$', HostLookupView.as_view(), name=''),
]
