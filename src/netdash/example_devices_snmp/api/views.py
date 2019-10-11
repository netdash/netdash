from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework import viewsets

from example_devices_snmp.models import SnmpDevice
from example_devices_snmp.api.serializers import SnmpDeviceSerializer


@method_decorator(
    permission_required('example_devices_snmp.can_view_module', raise_exception=True,),
    name='dispatch'
)
class DeviceViewSet(viewsets.ModelViewSet):
    """
    An interface to work with SNMP devices.
    """
    serializer_class = SnmpDeviceSerializer
    queryset = SnmpDevice.objects.all()
