from django.db import models


class ModulePermissions(models.Model):
    class Meta:
        managed = False
        default_permissions = []
        permissions = [
            ('can_view_module', 'Can see link in the NetDash navbar and access module.'),
        ]
