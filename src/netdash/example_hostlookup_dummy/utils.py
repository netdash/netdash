from typing import Iterable
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network, ip_network

from netaddr import EUI

from hostlookup_abstract.utils import HostLookupResult


def host_lookup(q='') -> Iterable[HostLookupResult]:
    if not q:
        return []
    query_network = ip_network(q, False)
    ipv4_a = query_network[0]\
        if isinstance(query_network, IPv4Network)\
        else IPv4Address('192.168.0.1')
    ipv6_a = query_network[0]\
        if isinstance(query_network, IPv6Network)\
        else IPv6Address('2001:db8::')
    ipv4_b = query_network[-1]\
        if isinstance(query_network, IPv4Network)\
        else IPv4Address('192.168.0.2')
    ipv6_b = query_network[-1]\
        if isinstance(query_network, IPv6Network)\
        else None
    return [
        HostLookupResult(
            EUI('00:0a:95:9d:68:16'),
            ipv4_a,
            ipv6_a,
            datetime.now(),
            'd-BLDG-1',
            IPv4Address('192.168.255.0'),
            IPv6Address('2002:db8::'),
            '1099999, GREAT NEW BUILDING (1000 BUILDING PL), B, B111 G02',
        ),
        HostLookupResult(
            EUI('00:0a:95:9d:68:17'),
            ipv4_b,
            ipv6_b,
            datetime.now(),
            'd-BLDG-1',
            IPv4Address('192.168.255.1'),
            None,
            '1099999, GREAT NEW BUILDING (1000 BUILDING PL), B, B111 G02',
        ),
    ]
