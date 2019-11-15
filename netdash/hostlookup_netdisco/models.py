from django.db import models
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator


class ModulePermissions(models.Model):
    class Meta:
        managed = False
        default_permissions = []
        permissions = [
            ('can_view_module', 'Can see link in the NetDash navbar and access module.'),
        ]


can_view_permission = permission_required("hostlookup_netdisco.can_view_module", raise_exception=True)


can_view_permission_dispatch = method_decorator(can_view_permission, name='dispatch')
