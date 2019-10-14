from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets


DATA = [
    'one',
    'two',
    'three',
]


def get_full(pk, request):
    return {
        'hostname': DATA[pk],
        'url': reverse('devices-api:device-detail', args=[pk + 1], request=request),
    }


@method_decorator(
    permission_required('example_error_import.can_view_module', raise_exception=True,),
    name='dispatch'
)
class DeviceViewSet(viewsets.ViewSet):
    '''
    An interface to work with dummy devices
    '''

    basename = 'device'

    def list(self, request):
        return Response([
            get_full(i, request) for i, d in enumerate(DATA)
        ])

    def retrieve(self, request, pk):
        return Response(get_full(int(pk) - 1, request))
