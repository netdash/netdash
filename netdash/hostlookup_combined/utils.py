from typing import Iterable, Optional
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address, ip_address

from netaddr import EUI

from hostlookup_bluecat.utils import BlueCatHostLookupResult, transform as bc_transform
from hostlookup_bluecat.bluecat import lookup_cidr, get_connection
from hostlookup_netdisco.utils import host_lookup as nd_host_lookup


def host_lookup(q: str, bluecat_config: int) -> Iterable[BlueCatHostLookupResult]:
    with get_connection() as bc:
        bc_network = lookup_cidr(bc, ip_address(q), bluecat_config)
    bc_cidr = bc_network.network
    bc_results = [bc_transform(bca) for bca in bc_network.bc_addresses]
    nd_results = nd_host_lookup(str(bc_cidr))
    return merge(bc_results, nd_results)
