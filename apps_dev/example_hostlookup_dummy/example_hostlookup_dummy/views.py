from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from hostlookup_abstract.views import BaseHostLookupView
from .utils import host_lookup


@method_decorator(
    permission_required("example_hostlookup_dummy.can_view_module", raise_exception=True),
    name='dispatch'
)
class HostLookupView(BaseHostLookupView):
    def host_lookup(self):
        q = self.request.GET.get('q', '')
        return host_lookup(q)
