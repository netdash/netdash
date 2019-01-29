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
        'url': reverse('device-detail', args=[pk + 1], request=request),
    }


class DeviceViewSet(viewsets.ViewSet):
    '''
    An interface to work with dummy devices
    '''

    def list(self, request):
        return Response([
            get_full(i, request) for i, d in enumerate(DATA)
        ])

    def retrieve(self, request, pk):
        return Response(get_full(int(pk) - 1, request))
