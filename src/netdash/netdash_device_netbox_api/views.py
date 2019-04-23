import requests

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets

if not settings.NETBOX_API_URL:
    raise ImproperlyConfigured(
        'NETBOX_API_URL to use netdash_device_netbox_api')

URL = settings.NETBOX_API_URL.lstrip('/')


class DeviceViewSet(viewsets.ViewSet):
    '''
    An interface to work with NetBox devices
    '''

    def list(self, request):
        r = requests.get(URL + '/dcim/devices/')
        devices = r.json()['results']

        return Response([
            {
                'hostname': x['name'],
                'url': reverse(
                    'device-detail', args=[x['id']], request=request),
            } for x in devices])

    def retrieve(self, request, pk):
        r = requests.get(URL + '/dcim/devices/' + pk + '/')
        device = r.json()

        return Response({
                'hostname': device['name'],
                'url': reverse(
                    'device-detail', args=[device['id']], request=request),
            })
