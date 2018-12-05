from netdash_device_snmp.models import SnmpDevice
from netdash_device_snmp.serializers import SnmpDeviceSerializer

from rest_framework import viewsets


class DeviceViewSet(viewsets.ModelViewSet):
    """
    An interface to work with SNMP devices.
    """
    serializer_class = SnmpDeviceSerializer
    queryset = SnmpDevice.objects.all()

