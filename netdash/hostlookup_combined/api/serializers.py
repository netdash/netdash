from rest_framework import serializers

from hostlookup_bluecat.api.serializers import BlueCatHostLookupResponseSerializer as BlueCatSerializer
from hostlookup_abstract.api.serializers import HostLookupResponseSerializer as NetDiscoSerializer


class CombinedHostLookupResponseSerializer(serializers.Serializer):
    netdisco = NetDiscoSerializer(many=True)
    bluecat = BlueCatSerializer(many=True)
