from hostlookup_abstract.api.views import BaseHostView
from example_hostlookup_dummy.utils import host_lookup


class HostView(BaseHostView):
    def host_lookup(self, request, q=''):
        return host_lookup(q)
