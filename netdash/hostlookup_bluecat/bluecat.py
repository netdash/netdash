from typing import List, Union, Optional
from dataclasses import dataclass
from ipaddress import IPv4Network, IPv6Network, IPv4Address, IPv6Address, ip_address, ip_network

from django.conf import settings

from netaddr import EUI
from bluecat_bam import BAM


def get_connection():
    return BAM(settings.BAM_SERVER, settings.BAM_USERNAME, settings.BAM_PASSWORD)


@dataclass
class BlueCatConfiguration:
    bcid: int
    name: str
    description: str
    sharedNetwork: Optional[int]


def lookup_configurations(conn: BAM) -> List[BlueCatConfiguration]:
    r = conn.do('getEntities', parentId=0, type='Configuration', start=0, count=9999)
    return [
        BlueCatConfiguration(
            bcc['id'],
            bcc['name'],
            bcc['properties']['description'],
            (int(bcc['properties'].get('sharedNetwork'))
                if bcc['properties'].get('sharedNetwork')
                else None)
        ) for bcc in r
    ]


@dataclass
class BlueCatAddress:
    bcid: int
    name: str
    address: Union[IPv4Address, IPv6Address]
    state: str  # 3.8: Literal["DHCP_FREE", "DHCP_RESERVED", "DHCP_ALLOCATED", "RESERVED", "STATIC", "GATEWAY"]
    mac: Optional[EUI]
    hostnames: List[str]


@dataclass
class BlueCatNetwork:
    bcid: int
    name: str
    network: Union[IPv4Network, IPv6Network]
    gateway: Union[IPv4Address, IPv6Address]
    bc_addresses: List[BlueCatAddress]


def lookup_cidr(conn: BAM, ip: Union[IPv4Address, IPv6Address], container_bcid: int) -> BlueCatNetwork:
    entity_type = 'IP4Network' if isinstance(ip, IPv4Address) else 'IP6Network'
    resp = conn.do('getIPRangedByIP', containerId=container_bcid, type=entity_type, address=str(ip))
    print(resp)
    return BlueCatNetwork(
        resp['id'],
        resp['name'],
        ip_network(resp['properties']['CIDR'], False),
        ip_address(resp['properties'].get('gateway')) if resp['properties'].get('gateway') else None,
        lookup_ips(conn, resp['id'])
    )


def lookup_ips(conn: BAM, network_bcid: int) -> List[BlueCatAddress]:
    resp = conn.do('getEntities', parentId=network_bcid, type='IP4Address', start=0, count=9999)
    return [
        BlueCatAddress(
            ip['id'],
            ip['name'],
            ip_address(ip['properties']['address']),
            ip['properties']['state'],
            EUI(ip['properties']['macAddress']) if ip['properties'].get('macAddress') else None,
            lookup_hostnames(conn, ip['id'])
        ) for ip in resp
        if ip['properties']['state'].upper() in {'STATIC', 'DHCP_RESERVED'}
    ]


def lookup_hostnames(conn: BAM, ip_bcid: int) -> List[str]:
    resp = conn.do('getLinkedEntities', entityId=ip_bcid, type='HostRecord', start=0, count=9999)
    return [r['properties']['absoluteName'] for r in resp]
