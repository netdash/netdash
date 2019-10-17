from typing import Iterable, List, Dict, Union, Optional
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address, ip_address

from netaddr import EUI

from hostlookup_bluecat.bluecat import lookup_cidr, get_connection, BlueCatAddress


@dataclass
class BlueCatHostLookupResult:
    mac: EUI
    ipv4: Optional[IPv4Address]
    ipv6: Optional[IPv6Address]
    hostnames: str

def transform(bca: BlueCatAddress) -> BlueCatHostLookupResult:
    return BlueCatHostLookupResult(
        bca.mac,
        bca.address,
        None,
        ', '.join(bca.hostnames)
    )

def host_lookup(q='') -> Iterable[BlueCatHostLookupResult]:
    if not q:
        return []
    with get_connection() as bc:
        bc_network = lookup_cidr(bc, ip_address(q), 557057)
    return [transform(bca) for bca in bc_network.bc_addresses]
