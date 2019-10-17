from django.urls import path

from .views import HostLookupView

app_name = 'hostlookup'
urlpatterns = [
    path(r'', HostLookupView.as_view(), name='index'),
]
