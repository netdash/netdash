from netdash_device_snmp.models import SnmpDevice
from netdash_device_snmp.serializers import SnmpDeviceSerializer

from rest_framework import viewsets


class DeviceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = SnmpDeviceSerializer
    queryset = SnmpDevice.objects.all()

