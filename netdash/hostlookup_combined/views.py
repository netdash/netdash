from hostlookup_bluecat.views import HostLookupView as BlueCatHostLookupView
from .utils import host_lookup


class HostLookupView(BlueCatHostLookupView):
    template_name = "hostlookup_combined/hostlookupresult_list.html"

    def host_lookup(self):
        q = self.request.GET.get('q', '')
        if not q:
            return None
        bluecat_config = self.request.GET.get('bluecat_config', None)
        return host_lookup(q, bluecat_config)
