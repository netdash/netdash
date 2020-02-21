from django.urls import path

from .views import HostView

app_name = 'hostlookup-api'

urlpatterns = [
    path('', HostView.as_view(), name='host-lookup'),
]
