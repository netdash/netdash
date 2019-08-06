from ipaddress import IPv4Address, IPv6Address
from typing import Optional, Iterable
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime

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


class BaseHostLookupView(ABC, TemplateView):
    template_name = "hostlookup/hostlookupresult_list.html"

    @abstractmethod
    def host_lookup(self, **kwargs) -> Iterable[HostLookupResult]:
        return NotImplemented

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = self.host_lookup(**kwargs)
        context['results'] = results
        return context
