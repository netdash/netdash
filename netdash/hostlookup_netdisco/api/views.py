from netdash_api.permissions import HasScopeOrPermission

from hostlookup_abstract.api.views import BaseHostView
from hostlookup_netdisco.utils import host_lookup


class HostView(BaseHostView):
    permission_classes = [HasScopeOrPermission]
    required_scopes = ['hostlookup_netdisco.can_view_module']

    def host_lookup(self, request, q=''):
        return host_lookup(q)
