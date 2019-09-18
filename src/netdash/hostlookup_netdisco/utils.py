from typing import Iterable
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network, ip_network

from netaddr import EUI

from hostlookup_abstract.utils import HostLookupResult
from netdisco.models import Device


def device_to_hostlookupresult(device: Device) -> HostLookupResult:
    ip = ip_network(device.ip)
    return HostLookupResult(
        device.mac,
        device.ip if isinstance(ip, IPv4Network) else None,
        device.ip if isinstance(ip, IPv6Network) else None,
        device.last_discover,
        device.name,
        None,  # TODO
        None,  # TODO
        device.location,
    )


def host_lookup(q='') -> Iterable[HostLookupResult]:
    if not q:
        return []
    ip_network(q, False)
    devices = list(Device.objects.raw("SELECT * FROM device WHERE device.ip <<= inet %s", [q]))
    return [device_to_hostlookupresult(d) for d in devices]
