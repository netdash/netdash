from ipaddress import IPv4Address, IPv6Address
from typing import Optional, Iterable
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime

from django.shortcuts import render
from django.views.generic.base import TemplateView

from netaddr import EUI


@dataclass
class HostLookupResult:
    mac: EUI
    ipv4: IPv4Address
    ipv6: Optional[IPv6Address]
    last_seen: datetime
    host_port_name: str
    switch_ipv4: IPv4Address
    switch_ipv6: Optional[IPv6Address]
    switch_location: str


class HostLookupView(ABC, TemplateView):
    template_name = "hostlookup/hostlookupresult_list.html"

    # @abstractmethod
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = self.host_lookup(**kwargs)
        context['results'] = results
        return context
