from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address

from netaddr import EUI


@dataclass
class HostLookupResult:
    mac: EUI
    ipv4: Optional[IPv4Address]
    ipv6: Optional[IPv6Address]
    last_seen: datetime
    host_port_name: str
    switch_ipv4: Optional[IPv4Address]
    switch_ipv6: Optional[IPv6Address]
    switch_location: str
