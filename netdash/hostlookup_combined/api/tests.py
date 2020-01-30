from unittest.mock import patch
import urllib
import json
from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission

from rest_framework.test import APIRequestFactory, force_authenticate
from oauth2_provider.models import AccessToken

from hostlookup_combined.api.views import HostView
from netdash.models import User
from hostlookup_bluecat.tests import mock_lookup_cidr
from hostlookup_netdisco.tests import mock_fetch_as_dicts


@patch('hostlookup_combined.api.views.get_connection')
@patch('hostlookup_bluecat.utils.get_connection')
@patch('hostlookup_netdisco.utils.connections')
@patch('hostlookup_netdisco.utils.fetch_as_dicts', mock_fetch_as_dicts)
@patch('hostlookup_bluecat.utils.lookup_cidr', mock_lookup_cidr)
@patch('hostlookup_combined.api.views.lookup_cidr', mock_lookup_cidr)
class HostlookupCombinedAPITests(TestCase):

    def setUp(self):
        u = User.objects.create_user('networker', password='qwerty')  # nosec
        u.user_permissions.add(
            Permission.objects.get_by_natural_key('can_view_module', 'hostlookup_combined', 'modulepermissions')
        )
        User.objects.create_user('no_permissions', password='qwerty')  # nosec

    def _get_index(self):
        return self.client.get(reverse('hostlookup_combined-api:host-lookup'))

    def _get_base_request(self, **kwargs):
        f = APIRequestFactory()
        params = urllib.parse.urlencode(kwargs)
        return f.get(f'{reverse("hostlookup_combined-api:host-lookup")}?{str(params)}')

    def _get_index_view(self, **kwargs):
        r = self._get_base_request(**kwargs)
        r.user = User.objects.get_by_natural_key('networker')
        return HostView.as_view()(r)

    def test_renders_results(self, views_get_connection, utils_get_connection, connections):
        response = self._get_index_view(q='10.10.10.10', bluecat_config='1')
        response.render()
        data = json.loads(response.content)
        self.assertEqual(data['bluecat'][0]['mac'], '96-32-80-E1-3B-CF')
        self.assertEqual(data['bluecat'][0]['ipv4'], '141.100.0.0')
        self.assertEqual(data['bluecat'][0]['hostnames'][0], 'example.com')
        self.assertEqual(data['bluecat'][0]['hostnames'][1], 'second.com')
        self.assertEqual(data['bluecat'][1]['mac'], 'EE-03-A8-69-97-00')
        self.assertEqual(data['bluecat'][1]['ipv4'], '141.100.0.1')
        self.assertEqual(len(data['bluecat'][1]['hostnames']), 0)
        self.assertEqual(data['netdisco'][0]['mac'], '96-32-80-E1-3B-CF')
        self.assertEqual(data['netdisco'][0]['ipv4'], '141.100.0.0')
        self.assertEqual(data['netdisco'][0]['last_seen'], '2019-12-01T00:00:00')
        self.assertEqual(data['netdisco'][1]['mac'], 'EE-03-A8-69-97-00')
        self.assertEqual(data['netdisco'][1]['ipv4'], '141.100.0.1')
        self.assertEqual(data['netdisco'][1]['last_seen'], '2019-12-01T00:00:00')

    def test_view_denies_anonymous(self, views_get_connection, utils_get_connection, connections):
        response = self._get_index()
        self.assertEqual(response.status_code, 403)

    def test_view_denies_permissionless(self, views_get_connection, utils_get_connection, connections):
        self.client.login(username='no_permissions', password='qwerty')  # nosec
        response = self._get_index()
        self.assertEqual(response.status_code, 403)

    def test_view_denies_token_without_scopes(self, views_get_connection, utils_get_connection, connections):
        r = self._get_base_request(q='10.10.10.10', bluecat_config='1')
        no_scopes = AccessToken(
            expires=datetime.now().astimezone() + timedelta(days=365),
        )
        force_authenticate(r, token=no_scopes)
        response = HostView.as_view()(r)
        self.assertEqual(response.status_code, 403)

    def test_view_accepts_token_with_scopes(self, views_get_connection, utils_get_connection, connections):
        r = self._get_base_request(q='10.10.10.10', bluecat_config='1')
        scopes = AccessToken(
            expires=datetime.now().astimezone() + timedelta(days=365),
            scope='hostlookup_combined.can_view_module',
        )
        force_authenticate(r, token=scopes)
        response = HostView.as_view()(r)
        self.assertEqual(response.status_code, 200)
