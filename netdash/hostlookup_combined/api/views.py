from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework.response import Response
from rest_framework import viewsets


@method_decorator(
    permission_required('hostlookup_combined.can_view_module', raise_exception=True,),
    name='dispatch'
)
class HostlookupCombinedViewSet(viewsets.ViewSet):
    '''
    Describe your API here.
    '''

    def list(self, request):
        return Response(['zero', 'one', 'two'])

    def retrieve(self, request, pk):
        return Response(['zero', 'one', 'two'][int(pk)])
