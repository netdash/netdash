from rest_framework import serializers


class HostLookupResponseSerializer(serializers.Serializer):
    mac = serializers.CharField(required=False)
    ipv4 = serializers.IPAddressField(required=False)
    ipv6 = serializers.IPAddressField(required=False)
    hostnames = serializers.ListField(child=serializers.CharField(), required=False)
