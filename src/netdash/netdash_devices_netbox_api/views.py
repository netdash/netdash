import requests

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets


class DeviceViewSet(viewsets.ViewSet):
    '''
    An interface to work with NetBox devices
    '''

    basename = 'device'

    def __init__(self, *args, **kwargs):
        if not settings.NETBOX_API_URL:
            raise ImproperlyConfigured(
                'NETBOX_API_URL to use netdash_device_netbox_api')
        self.URL = settings.NETBOX_API_URL.lstrip('/')
        super().__init__(*args, **kwargs)

    def list(self, request):
        print('url', self.URL)
        r = requests.get(self.URL + '/dcim/devices/')
        devices = r.json()['results']
        return Response([
            {
                'hostname': x['name'],
                'url': reverse(
                    'device-detail', args=[x['id']], request=request),
            } for x in devices])

    def retrieve(self, request, pk):
        r = requests.get(self.URL + '/dcim/devices/' + pk + '/')
        device = r.json()
        return Response({
                'hostname': device['name'],
                'url': reverse(
                    'device-detail', args=[device['id']], request=request),
            })
