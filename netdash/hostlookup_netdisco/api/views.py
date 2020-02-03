from hostlookup_abstract.api.views import BaseHostView
from hostlookup_netdisco.utils import host_lookup

from .permissions import HasScopeOrPermission


class HostView(BaseHostView):
    permission_classes = [HasScopeOrPermission]
    required_scopes = ['hostlookup_netdisco.can_view_module']

    def host_lookup(self, request, q=''):
        return host_lookup(q)
