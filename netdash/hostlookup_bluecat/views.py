from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from hostlookup_abstract.views import BaseHostLookupView
from .utils import host_lookup
from .bluecat import lookup_configurations, get_connection


@method_decorator(
    permission_required("hostlookup_bluecat.can_view_module", raise_exception=True),
    name='dispatch'
)
class HostLookupView(BaseHostLookupView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with get_connection() as bc:
            bluecat_configs = lookup_configurations(bc)
        context['bluecat_configs'] = bluecat_configs
        return context

    def host_lookup(self):
        q = self.request.GET.get('q', '')
        if not q:
            return []
        bluecat_config = self.request.GET.get('bluecat_config', None)
        return host_lookup(q, bluecat_config)
