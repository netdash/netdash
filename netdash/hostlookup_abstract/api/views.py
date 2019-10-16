from abc import ABC, abstractmethod
from typing import Iterable
from dataclasses import asdict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import HostLookupResponseSerializer
from hostlookup_abstract.utils import HostLookupResult


class BaseHostView(ABC, APIView):
    @abstractmethod
    def host_lookup(self, request, q='') -> Iterable[HostLookupResult]:
        return NotImplemented

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, description='Host lookup query term.', type=openapi.TYPE_STRING),
        ],
        responses={status.HTTP_200_OK: HostLookupResponseSerializer(many=True)},
    )
    def get(self, request):
        q = request.query_params.get('q', '')
        return Response([asdict(r) for r in self.host_lookup(request, q)])
