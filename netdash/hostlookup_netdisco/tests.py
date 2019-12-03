from typing import List, Dict
from unittest.mock import patch
import urllib
import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.test.client import RequestFactory

from netdash.models import User
from hostlookup_netdisco.views import HostLookupView


def mock_fetch_as_dicts(cursor) -> List[Dict]:
    return [
        {
            'mac': '96:32:80:e1:3b:cf',
            'ip': '141.100.0.0',
            'name': 's-BLDG-1',
            'switch': '10.10.0.0',
            'time_last': datetime.datetime(2019, 12, 1),
            'location': 'Big Building F1',
        },
        {
            'mac': 'ee:03:a8:69:97:00',
            'ip': '141.100.0.1',
            'name': 's-BLDG-1',
            'switch': '10.10.0.0',
            'time_last': datetime.datetime(2019, 12, 1),
            'location': 'Big Building F1',
        },
    ]


@patch('hostlookup_netdisco.utils.connections')
@patch('hostlookup_netdisco.utils.fetch_as_dicts', mock_fetch_as_dicts)
class HostlookupNetDiscoTests(TestCase):

    def setUp(self):
        u = User.objects.create_user('networker', password='qwerty')
        u.user_permissions.add(
            Permission.objects.get_by_natural_key('can_view_module', 'hostlookup_netdisco', 'modulepermissions')
        )

    def _login(self):
        self.client.login(username='networker', password='qwerty')  # nosec

    def _get_index(self):
        return self.client.get(reverse('hostlookup_bluecat:index'))

    def _get_index_view(self, **kwargs):
        f = RequestFactory()
        params = urllib.parse.urlencode(kwargs)
        r = f.get(f'{reverse("hostlookup_netdisco:index")}?{str(params)}')
        r.user = User.objects.get_by_natural_key('networker')
        return HostLookupView.as_view()(r)

    def test_renders_form(self, connections):
        response = self._get_index_view()
        response.render()
        self.assertContains(response, '<form')
        self.assertContains(response, '<button type="submit"')
        self.assertContains(
            response,
            '<input type="text"'
        )

    def test_renders_form_selections(self, connections):
        response = self._get_index_view(q='10.10.10.10')
        response.render()
        self.assertContains(
            response,
            '<input type="text" class="form-control" name="q" placeholder="Search..." value="10.10.10.10" />'
        )

    def test_renders_results(self, connections):
        response = self._get_index_view(q='10.10.10.10')
        response.render()
        self.assertContains(response, '<table')
        self.assertContains(response, '<th>IPv4</th>')
        self.assertContains(response, '141.100.0.0')
        # Renders order for IPv4 141.100.0.1
        self.assertContains(response, '<td data-order="2372141057">')

    def test_renders_ip_error(self, connections):
        response = self._get_index_view(q='foobar')
        response.render()
        self.assertContains(response, 'does not appear to be an IPv4 or IPv6 network')

    def test_view_permission_required(self, connections):
        response = self._get_index()
        self.assertEqual(response.status_code, 403)
