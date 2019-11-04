from typing import Dict
from ipaddress import ip_address
from dataclasses import asdict

from hostlookup_bluecat.utils import transform as bc_transform
from hostlookup_bluecat.bluecat import lookup_cidr, get_connection
from hostlookup_netdisco.utils import host_lookup as nd_host_lookup
from .merge import MergedTable


def host_lookup(q: str, bluecat_config: int) -> Dict:
    with get_connection() as bc:
        bc_network = lookup_cidr(bc, ip_address(q), bluecat_config)
    bc_cidr = bc_network.network
    bc_results = [asdict(bc_transform(bca)) for bca in bc_network.bc_addresses if bca.mac]
    nd_results = [asdict(nd) for nd in nd_host_lookup(str(bc_cidr)) if nd.mac]
    columns = [
        ('mac', 'MAC Address'),
        ('ipv4', 'IPv4'),
        ('ipv6', 'IPv6'),
        ('last_seen', 'Last Seen'),
        ('switch_ipv4', 'Switch IPv4'),
        ('switch_ipv6', 'Switch IPv6'),
        ('host_port_name', 'Host Port Name'),
        ('switch_location', 'Switch Location'),
        ('hostnames', 'Hostnames'),
    ]
    return MergedTable('mac', columns, bluecat=bc_results, netdisco=nd_results)
