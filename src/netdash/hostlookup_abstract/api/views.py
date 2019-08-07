from abc import ABC, abstractmethod
from typing import Iterable
from dataclasses import asdict

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework.response import Response
from rest_framework import viewsets

from hostlookup_abstract.utils import HostLookupResult


@method_decorator(
    permission_required('example_hostlookup_dummy.can_view_module', raise_exception=True,),
    name='dispatch'
)
class BaseHostViewSet(ABC, viewsets.ViewSet):
    basename = 'host'

    @abstractmethod
    def host_lookup(self, request) -> Iterable[HostLookupResult]:
        return NotImplemented

    def list(self, request):
        return Response([asdict(r) for r in self.host_lookup(request)])
