from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from hostlookup_abstract.api.views import BaseHostView
from hostlookup_netdisco.utils import host_lookup


@method_decorator(
    permission_required("hostlookup_netdisco.can_view_module", raise_exception=True),
    name='dispatch'
)
class HostView(BaseHostView):
    def host_lookup(self, request, q=''):
        return host_lookup(q)
