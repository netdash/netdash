from unittest.mock import MagicMock
from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth.models import Permission, ContentType

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.request import Request
from oauth2_provider.models import AccessToken

from netdash.models import User
from .permissions import HasScopeOrPermission


class HasScopeOrPermissionTests(TestCase):
    def setUp(self):
        self.permission = HasScopeOrPermission()
        ct = ContentType.objects.get(app_label='netdash', model='user')
        a = Permission.objects.create(codename='a', name='A', content_type=ct)
        b = Permission.objects.create(codename='b', name='B', content_type=ct)
        self.user_a = User.objects.create_user('user_a')
        self.user_a.user_permissions.add(a)
        self.user_b = User.objects.create_user('user_b')
        self.user_b.user_permissions.add(b)
        self.user_both = User.objects.create_user('user_both')
        self.user_both.user_permissions.add(a, b)
        self.user_none = User.objects.create_user('user_none')
        self.token_a = AccessToken(
            expires=datetime.now().astimezone() + timedelta(days=365),
            scope='netdash.a'
        )
        self.token_b = AccessToken(
            expires=datetime.now().astimezone() + timedelta(days=365),
            scope='netdash.b'
        )
        self.token_both = AccessToken(
            expires=datetime.now().astimezone() + timedelta(days=365),
            scope='netdash.a netdash.b'
        )
        self.token_none = AccessToken(
            expires=datetime.now().astimezone() + timedelta(days=365),
            scope=''
        )
        self.view = MagicMock(required_scopes=['netdash.a'])
        self.view_requires_two = MagicMock(required_scopes=['netdash.a', 'netdash.b'])
        self.request = APIRequestFactory().request()

    def test_allows_user_with_permission(self):
        force_authenticate(self.request, user=self.user_a)
        request = Request(self.request)
        self.assertTrue(self.permission.has_permission(request, self.view))

    def test_denies_user_without_permission(self):
        force_authenticate(self.request, user=self.user_none)
        request = Request(self.request)
        self.assertFalse(self.permission.has_permission(request, self.view))

    def test_denies_user_with_wrong_permission(self):
        force_authenticate(self.request, user=self.user_b)
        request = Request(self.request)
        self.assertFalse(self.permission.has_permission(request, self.view))

    def test_denies_user_without_all_permissions(self):
        force_authenticate(self.request, user=self.user_a)
        request = Request(self.request)
        self.assertFalse(self.permission.has_permission(request, self.view_requires_two))

    def test_allows_user_with_all_permissions(self):
        force_authenticate(self.request, user=self.user_both)
        request = Request(self.request)
        self.assertTrue(self.permission.has_permission(request, self.view_requires_two))

    def test_allows_token_with_scope(self):
        force_authenticate(self.request, token=self.token_a)
        request = Request(self.request)
        self.assertTrue(self.permission.has_permission(request, self.view))

    def test_denies_token_without_scope(self):
        force_authenticate(self.request, token=self.token_none)
        request = Request(self.request)
        self.assertFalse(self.permission.has_permission(request, self.view))

    def test_denies_token_wrong_scope(self):
        force_authenticate(self.request, token=self.token_b)
        request = Request(self.request)
        self.assertFalse(self.permission.has_permission(request, self.view))

    def test_denies_token_without_all_scopes(self):
        force_authenticate(self.request, token=self.token_a)
        request = Request(self.request)
        self.assertFalse(self.permission.has_permission(request, self.view_requires_two))

    def test_allows_token_with_all_scopes(self):
        force_authenticate(self.request, token=self.token_both)
        request = Request(self.request)
        self.assertTrue(self.permission.has_permission(request, self.view_requires_two))
