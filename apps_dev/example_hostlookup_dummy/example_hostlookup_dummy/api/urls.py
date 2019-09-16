from django.conf import settings
from django.urls import path

from rest_framework import routers

from .views import HostView

app_name = 'hostlookup-api'

urlpatterns = [
    path('', HostView.as_view(), name='host-lookup'),
]
