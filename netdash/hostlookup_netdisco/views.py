from hostlookup_abstract.views import BaseHostLookupView
from .utils import host_lookup


class HostLookupView(BaseHostLookupView):
    def host_lookup(self):
        q = self.request.GET.get('q', '')
        return host_lookup(q)
