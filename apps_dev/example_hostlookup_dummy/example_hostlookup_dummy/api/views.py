from hostlookup_abstract.api.views import BaseHostViewSet
from example_hostlookup_dummy.utils import host_lookup


class HostViewSet(BaseHostViewSet):
    def host_lookup(self, request):
        return host_lookup()
