from hostlookup_abstract.views import BaseHostLookupView
from .utils import host_lookup


class HostLookupView(BaseHostLookupView):
    def host_lookup(self, **kwargs):
        return host_lookup()
