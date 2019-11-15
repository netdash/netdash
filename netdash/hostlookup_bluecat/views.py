from hostlookup_abstract.views import BaseHostLookupView
from .utils import host_lookup
from .bluecat import lookup_configurations, get_connection


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
            return None
        bluecat_config = self.request.GET.get('bluecat_config', None)
        return host_lookup(q, bluecat_config)
