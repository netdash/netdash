from oauth2_provider.scopes import BaseScopes
from django.contrib.auth.models import Permission


class PermissionsScopes(BaseScopes):
    def get_all_scopes(self):
        return {
            f'{p.content_type.app_label}.{p.codename}': str(p)
            for p in Permission.objects.all()
        }

    def get_available_scopes(self, application=None, request=None, *args, **kwargs):
        """
        Derives available scopes from all permissions in application.groups.all().
        """
        if not application:
            return []
        grouped_permissions = [g.permissions.all() for g in application.groups.all()]
        flattened_permissions = [p for permissions in grouped_permissions for p in permissions]
        return [f'{p.content_type.app_label}.{p.codename}' for p in flattened_permissions]

    def get_default_scopes(self, application=None, request=None, *args, **kwargs):
        return []
