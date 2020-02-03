from django.test import TestCase

from django.contrib.auth.models import Permission, Group

from netdash.scopes import PermissionsScopes
from netdash.models import Application


class PermissionsScopesTests(TestCase):
    def setUp(self):
        permission_a = Permission.objects.get_by_natural_key(
            'can_view_module', 'hostlookup_netdisco', 'modulepermissions'
        )
        permission_b = Permission.objects.get_by_natural_key(
            'can_view_module', 'hostlookup_bluecat', 'modulepermissions'
        )
        permission_c = Permission.objects.get_by_natural_key(
            'can_view_module', 'hostlookup_combined', 'modulepermissions'
        )
        group_a = Group.objects.create(
            name='a'
        )
        group_a.permissions.set([permission_a, permission_c])
        group_a.save()
        group_b = Group.objects.create(
            name='b'
        )
        group_b.permissions.set([permission_b])
        group_b.save()
        self.has_groups = Application.objects.create(
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
            name='has_groups',
        )
        self.has_groups.groups.set([group_a, group_b])
        self.has_groups.save()
        self.no_groups = Application.objects.create(
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
            name='no_groups'
        )

    def test_gets_all_scopes(self):
        ps = PermissionsScopes()
        all_scopes = ps.get_all_scopes()
        self.assertIn('hostlookup_netdisco.can_view_module', all_scopes.keys())
        self.assertIn('hostlookup_bluecat.can_view_module', all_scopes.keys())
        self.assertIn('hostlookup_combined.can_view_module', all_scopes.keys())

    def test_groups_scopes_available(self):
        ps = PermissionsScopes()
        available = ps.get_available_scopes(application=self.has_groups)
        self.assertIn('hostlookup_netdisco.can_view_module', available)
        self.assertIn('hostlookup_bluecat.can_view_module', available)
        self.assertIn('hostlookup_combined.can_view_module', available)

    def test_scopes_unavailable(self):
        ps = PermissionsScopes()
        available = ps.get_available_scopes(application=self.no_groups)
        self.assertNotIn('hostlookup_netdisco.can_view_module', available)
        self.assertNotIn('hostlookup_bluecat.can_view_module', available)
        self.assertNotIn('hostlookup_combined.can_view_module', available)

    def test_no_default_scopes(self):
        ps = PermissionsScopes()
        default = ps.get_default_scopes()
        self.assertEqual(len(default), 0)
