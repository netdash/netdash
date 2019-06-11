import requests

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets

from netdash_devices_netbox_api.utils import get_device, get_devices


class DeviceViewSet(viewsets.ViewSet):
    '''
    An interface to work with NetBox devices
    '''

    def __init__(self, *args, **kwargs):
        if not settings.NETBOX_API_URL:
            raise ImproperlyConfigured('NETBOX_API_URL to use netdash_devices_netbox_api')
        self.URL = settings.NETBOX_API_URL.lstrip('/')
        super().__init__(*args, **kwargs)

    def list(self, request):
        devices = get_devices(self.URL)
        return Response([
            {
                'hostname': x['name'],
                'url': reverse(
                    'devices-api:device-detail', args=[x['id']], request=request),
            } for x in devices])

    def retrieve(self, request, pk):
        device = get_device(self.URL, pk)
        return Response({
                'hostname': device['name'],
                'url': reverse(
                    'devices-api:device-detail', args=[device['id']], request=request),
            })



