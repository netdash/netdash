from abc import ABC, abstractmethod
from typing import Iterable
from dataclasses import asdict

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import BaseFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from hostlookup_abstract.utils import HostLookupResult


@method_decorator(
    permission_required('example_hostlookup_dummy.can_view_module', raise_exception=True,),
    name='dispatch'
)
class BaseHostView(ABC, APIView):
    @abstractmethod
    def host_lookup(self, request, q='') -> Iterable[HostLookupResult]:
        return NotImplemented

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, description='Host lookup query term.', type=openapi.TYPE_STRING),
        ],
        # responses={status.HTTP_200_OK: HostLookupResponseSerializer}
    )
    def get(self, request):
        q = request.query_params.get('q', '')
        return Response([asdict(r) for r in self.host_lookup(request, q)])
