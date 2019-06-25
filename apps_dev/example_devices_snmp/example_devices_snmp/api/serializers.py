from rest_framework import serializers

from example_devices_snmp.models import SnmpDevice


class SnmpDeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SnmpDevice
        fields = '__all__'
