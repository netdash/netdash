from typing import Union, List
from ipaddress import IPv4Address, IPv6Address, ip_network, ip_address
from unittest.mock import patch
import urllib

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.test.client import RequestFactory

from netdash.models import User
from bluecat_bam import BAM
from hostlookup_bluecat.bluecat import BlueCatNetwork, BlueCatAddress, BlueCatConfiguration
from hostlookup_bluecat.views import HostLookupView

from netaddr import EUI


def mock_lookup_cidr(conn: BAM, ip: Union[IPv4Address, IPv6Address], container_bcid: int) -> BlueCatNetwork:
    nw = ip_network('141.100.0.0/30')
    return BlueCatNetwork(
        777,
        'my_network',
        nw,
        ip_address('10.10.10.10'),
        [
            BlueCatAddress(
                0,
                'first',
                nw[0],
                'DHCP_RESERVED',
                EUI('96:32:80:e1:3b:cf'),
                ['example.com', 'second.com'],
            ),
            BlueCatAddress(
                1,
                'second',
                nw[1],
                'DHCP_RESERVED',
                EUI('ee:03:a8:69:97:00'),
                [],
            ),
            BlueCatAddress(
                2,
                'third',
                nw[2],
                'DHCP_RESERVED',
                EUI('9e:2c:f0:5e:c3:3f'),
                [],
            ),
            BlueCatAddress(
                3,
                'fourth',
                nw[3],
                'DHCP_RESERVED',
                EUI('22:07:bb:ac:50:df'),
                [],
            ),
        ]
    )


def mock_lookup_cidr_empty(conn: BAM, ip: Union[IPv4Address, IPv6Address], container_bcid: int) -> BlueCatNetwork:
    nw = ip_network('141.100.0.0/30')
    return BlueCatNetwork(
        777,
        'my_network',
        nw,
        ip_address('10.10.10.10'),
        [],
    )


def mock_lookup_configurations(conn: BAM) -> List[BlueCatConfiguration]:
    return [
        BlueCatConfiguration(
            1,
            'default_config',
            'The default configuration.',
            None,
        ),
        BlueCatConfiguration(
            2,
            'other_config',
            'Another configuration.',
            None,
        ),
    ]


@patch('hostlookup_bluecat.views.get_connection')
@patch('hostlookup_bluecat.utils.get_connection')
@patch('hostlookup_bluecat.views.lookup_configurations', mock_lookup_configurations)
@patch('hostlookup_bluecat.utils.lookup_cidr', mock_lookup_cidr)
class HostlookupBlueCatTests(TestCase):

    def setUp(self):
        u = User.objects.create_user('networker', password='qwerty')
        u.user_permissions.add(
            Permission.objects.get_by_natural_key('can_view_module', 'hostlookup_bluecat', 'modulepermissions')
        )

    def _login(self):
        self.client.login(username='networker', password='qwerty')  # nosec

    def _get_index(self):
        return self.client.get(reverse('hostlookup_bluecat:index'))

    def _get_index_view(self, **kwargs):
        f = RequestFactory()
        params = urllib.parse.urlencode(kwargs)
        r = f.get(f'{reverse("hostlookup_bluecat:index")}?{str(params)}')
        r.user = User.objects.get_by_natural_key('networker')
        return HostLookupView.as_view()(r)

    @patch('hostlookup_bluecat.utils.lookup_cidr', mock_lookup_cidr_empty)
    def test_renders_form(self, views_get_connection, utils_get_connection):
        response = self._get_index_view()
        response.render()
        self.assertContains(response, '<form')
        self.assertContains(response, '<button type="submit"')
        self.assertContains(
            response,
            '<select name="bluecat_config" class="col-lg-3 custom-select" value="">'
        )
        self.assertContains(
            response,
            '<input type="text"'
        )
        self.assertContains(response, '<option value="1"')
        self.assertContains(response, '<option value="2"')

    def test_renders_form_selections(self, views_get_connection, utils_get_connection):
        response = self._get_index_view(q='10.10.10.10', bluecat_config='1')
        response.render()
        self.assertContains(
            response,
            '<select name="bluecat_config" class="col-lg-3 custom-select" value="1">'
        )
        self.assertContains(
            response,
            '<input type="text" class="form-control" name="q" placeholder="Search..." value="10.10.10.10" />'
        )

    def test_renders_results(self, views_get_connection, utils_get_connection):
        response = self._get_index_view(q='10.10.10.10', bluecat_config='1')
        response.render()
        self.assertContains(response, '<table')
        self.assertContains(response, '<th>IPv4</th>')
        self.assertContains(response, '141.100.0.0')
        # Renders order for IPv4 141.100.0.1
        self.assertContains(response, '<td data-order="2372141057">')
        self.assertContains(response, 'example.com')
        self.assertContains(response, 'second.com')

    def test_renders_ip_error(self, views_get_connection, utils_get_connection):
        response = self._get_index_view(q='foobar', bluecat_config='1')
        response.render()
        self.assertContains(response, 'does not appear to be an IPv4 or IPv6 address')

    def test_view_permission_required(self, views_get_connection, utils_get_connection):
        response = self._get_index()
        self.assertEqual(response.status_code, 403)
