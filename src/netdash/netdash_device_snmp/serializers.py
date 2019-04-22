from rest_framework import serializers

from .models import SnmpDevice


class SnmpDeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SnmpDevice
        fields = '__all__'
