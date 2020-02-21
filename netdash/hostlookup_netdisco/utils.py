from typing import Iterable, List, Dict, Optional
from ipaddress import IPv4Address, IPv6Address, ip_address, ip_network

from django.db import connections
from django.core.exceptions import ValidationError

from netaddr import EUI

from hostlookup_abstract.utils import HostLookupResult


SQL = """
SELECT nip.ip
    ,nip.time_last
    ,n.mac
    ,n.switch
    ,d.location
    ,dp.name
FROM node_ip nip
    ,node n
    ,device d
    ,device_port dp
WHERE nip.ip <<= %s
    AND n.mac = nip.mac
    AND n.time_last = (
        SELECT max(time_last)
        FROM node
        WHERE active = 'true'
            AND mac = nip.mac
    )
    AND n.switch = d.ip
    AND n.switch = dp.ip
    AND REGEXP_REPLACE(n.port, '\\.0$', '') = dp.port
ORDER BY nip.ip
    ,nip.time_last
"""


def dict_to_hostlookupresult(d: Dict) -> HostLookupResult:
    ip = ip_address(d['ip'])
    switch_ip = ip_address(d['switch'])
    return HostLookupResult(
        EUI(d['mac']),
        ip if isinstance(ip, IPv4Address) else None,
        ip if isinstance(ip, IPv6Address) else None,
        d['time_last'],
        d['name'],
        switch_ip if isinstance(switch_ip, IPv4Address) else None,
        switch_ip if isinstance(switch_ip, IPv6Address) else None,
        d['location'],
    )


def distinct_by_ip(dicts: Iterable[Dict]) -> Iterable[Dict]:
    return {d['ip']: d for d in dicts}.values()


def fetch_as_dicts(cursor) -> List[Dict]:
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def host_lookup(q='') -> Optional[Iterable[HostLookupResult]]:
    if not q:
        return None
    try:
        ip_network(q, False)
    except ValueError as ve:
        raise ValidationError(ve)
    with connections['netdisco'].cursor() as cursor:
        cursor.execute(SQL, [q])
        results = distinct_by_ip(fetch_as_dicts(cursor))
    return [dict_to_hostlookupresult(r) for r in results]
