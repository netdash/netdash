from ipaddress import IPv4Address, IPv6Address
from typing import Optional, Iterable
from datetime import datetime

from netaddr import EUI

from hostlookup_abstract.views import BaseHostLookupView, HostLookupResult


class HostLookupView(BaseHostLookupView):
    def host_lookup(self, **kwargs) -> Iterable[HostLookupResult]:
        return [
            HostLookupResult(
                EUI('00:0a:95:9d:68:16'),
                IPv4Address('192.168.0.1'),
                IPv6Address('2001:db8::'),
                datetime.now(),
                'd-BLDG-1',
                IPv4Address('192.168.255.0'),
                IPv6Address('2002:db8::'),
                '1099999, GREAT NEW BUILDING (1000 BUILDING PL), B, B111 G02',
            ),
            HostLookupResult(
                EUI('00:0a:95:9d:68:17'),
                IPv4Address('192.168.0.2'),
                None,
                datetime.now(),
                'd-BLDG-1',
                IPv4Address('192.168.255.1'),
                None,
                '1099999, GREAT NEW BUILDING (1000 BUILDING PL), B, B111 G02',
            ),
        ]
