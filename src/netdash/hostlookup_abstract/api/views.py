from abc import ABC, abstractmethod
from typing import Iterable
from dataclasses import asdict

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets

from hostlookup_abstract.utils import HostLookupResult


class BaseHostViewSet(ABC, viewsets.ViewSet):
    basename = 'host'

    @abstractmethod
    def host_lookup(self, request) -> Iterable[HostLookupResult]:
        return NotImplemented

    def list(self, request):
        return Response([asdict(r) for r in self.host_lookup(request)])
