from dataclasses import asdict

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from hostlookup_abstract.api.views import BaseHostView
from hostlookup_bluecat.utils import host_lookup

from .serializers import HostLookupResponseSerializer


class HostView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, description='Host lookup query term.', type=openapi.TYPE_STRING),
            openapi.Parameter('bluecat_config', openapi.IN_QUERY, description='ID of BlueCat Configuration.', type=openapi.TYPE_INTEGER),
        ],
        responses={status.HTTP_200_OK: HostLookupResponseSerializer(many=True)},
    )
    def get(self, request):
        q = request.query_params.get('q', '')
        bluecat_config = request.query_params.get('bluecat_config', '')
        return Response([asdict(r) for r in host_lookup(q, bluecat_config)])
