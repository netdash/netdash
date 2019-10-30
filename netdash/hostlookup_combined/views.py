from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from hostlookup_bluecat.views import HostLookupView as BlueCatHostLookupView
from .utils import host_lookup


@method_decorator(
    permission_required("hostlookup_combined.can_view_module", raise_exception=True),
    name='dispatch'
)
class HostLookupView(BlueCatHostLookupView):
    def host_lookup(self):
        q = self.request.GET.get('q', '')
        if not q:
            return []
        bluecat_config = self.request.GET.get('bluecat_config', None)
        return host_lookup(q, bluecat_config)
