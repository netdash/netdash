from typing import Dict, List
from ipaddress import ip_address

from hostlookup_bluecat.utils import BlueCatHostLookupResult, transform as bc_transform
from hostlookup_bluecat.bluecat import lookup_cidr, get_connection
from hostlookup_netdisco.utils import host_lookup as nd_host_lookup
from hostlookup_abstract.utils import HostLookupResult as NetDiscoHostLookupResult
from .merge import MergedRow


def merge(bc_results: BlueCatHostLookupResult, nd_results: NetDiscoHostLookupResult) -> List[MergedRow]:
    bc_results_by_mac = {bcr.mac: bcr for bcr in bc_results}
    nd_results_by_mac = {ndr.mac: ndr for ndr in nd_results}
    all_macs = bc_results_by_mac.keys() | nd_results_by_mac.keys()
    return [
        MergedRow(bluecat=bc_results_by_mac[mac], netdisco=nd_results_by_mac[mac])
        for mac in all_macs
    ]


def host_lookup(q: str, bluecat_config: int) -> Dict:
    with get_connection() as bc:
        bc_network = lookup_cidr(bc, ip_address(q), bluecat_config)
    bc_cidr = bc_network.network
    bc_results = [bc_transform(bca) for bca in bc_network.bc_addresses]
    nd_results = nd_host_lookup(str(bc_cidr))
    return merge(bc_results, nd_results)
