from rest_framework import serializers


class HostLookupResponseSerializer(serializers.Serializer):
    mac = serializers.CharField()
    ipv4 = serializers.IPAddressField()
    ipv6 = serializers.IPAddressField(required=False)
    last_seen = serializers.DateTimeField()
    host_port_name = serializers.CharField()
    switch_ipv4 = serializers.IPAddressField()
    switch_ipv6 = serializers.IPAddressField(required=False)
    switch_location = serializers.CharField()
