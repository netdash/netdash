from ipaddress import IPv4Address, IPv6Address

from rest_framework.renderers import JSONRenderer as DRFJSONRenderer
from rest_framework.utils import encoders

from netaddr import EUI


class JSONEncoder(encoders.JSONEncoder):
    stringable_types = (EUI, IPv4Address, IPv6Address,)

    def default(self, obj):
        if isinstance(obj, self.stringable_types):
            return str(obj)
        return super().default(obj)


class JSONRenderer(DRFJSONRenderer):
    '''
    JSON renderer that also encodes common network types.
    '''
    encoder_class = JSONEncoder
