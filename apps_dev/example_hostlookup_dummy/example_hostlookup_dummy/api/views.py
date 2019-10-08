from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from hostlookup_abstract.api.views import BaseHostView
from example_hostlookup_dummy.utils import host_lookup


@method_decorator(
    permission_required('example_hostlookup_dummy.can_view_module', raise_exception=True,),
    name='dispatch'
)
class HostView(BaseHostView):
    def host_lookup(self, request, q=''):
        return host_lookup(q)
