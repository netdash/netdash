from dataclasses import asdict
from ipaddress import ip_address

from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from hostlookup_bluecat.bluecat import lookup_cidr, get_connection
from hostlookup_bluecat.utils import host_lookup as bc_host_lookup
from hostlookup_netdisco.utils import host_lookup as nd_host_lookup

from .serializers import CombinedHostLookupResponseSerializer


@method_decorator(
    permission_required('hostlookup_combined.can_view_module', raise_exception=True,),
    name='dispatch'
)
class HostView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY,
                              description='Host lookup query term.',
                              type=openapi.TYPE_STRING),
            openapi.Parameter('bluecat_config', openapi.IN_QUERY,
                              description='ID of BlueCat Configuration.',
                              type=openapi.TYPE_INTEGER),
        ],
        responses={status.HTTP_200_OK: CombinedHostLookupResponseSerializer(many=True)},
    )
    def get(self, request):
        q = request.query_params.get('q', '')
        try:
            ip = ip_address(q)
        except ValueError as ve:
            raise ValidationError(ve)
        bluecat_config = request.query_params.get('bluecat_config', None)
        if bluecat_config is None:
            raise ValidationError('bluecat_config is required.')
        with get_connection() as bc:
            bc_network = lookup_cidr(bc, ip, bluecat_config)
        bc_cidr = bc_network.network
        bc_results = [asdict(r) for r in bc_host_lookup(q, bluecat_config)]
        nd_results = [asdict(nd) for nd in nd_host_lookup(str(bc_cidr))]
        return Response({
            'bluecat': bc_results,
            'netdisco': nd_results,
        })
