from django.test import TestCase

from .merge import MergedTable, MergedRow, MergedCell, SourceValue
from hostlookup_combined.templatetags.merge_tags import merged_table, merged_cell

from typing import Union, List, Dict
from ipaddress import IPv4Address, IPv6Address, ip_network, ip_address
from unittest.mock import patch
import urllib
import datetime

from django.urls import reverse
from django.contrib.auth.models import Permission
from django.test.client import RequestFactory

from netdash.models import User
from bluecat_bam import BAM
from hostlookup_bluecat.bluecat import BlueCatNetwork, BlueCatAddress, BlueCatConfiguration
from hostlookup_combined.views import HostLookupView

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


@patch('hostlookup_bluecat.views.get_connection')
@patch('hostlookup_combined.utils.get_connection')
@patch('hostlookup_netdisco.utils.connections')
@patch('hostlookup_netdisco.utils.fetch_as_dicts', mock_fetch_as_dicts)
@patch('hostlookup_bluecat.views.lookup_configurations', mock_lookup_configurations)
@patch('hostlookup_combined.utils.lookup_cidr', mock_lookup_cidr)
class HostlookupCombinedTests(TestCase):

    def setUp(self):
        u = User.objects.create_user('networker', password='qwerty')
        p = Permission.objects.get_by_natural_key('can_view_module', 'hostlookup_combined', 'modulepermissions')
        # print('permission:', p)
        u.user_permissions.add(
            p
        )
        # print('user permissions:', u.user_permissions.all())

    def _login(self):
        self.client.login(username='networker', password='qwerty')

    def _get_index(self):
        return self.client.get(reverse('hostlookup_combined:index'))

    def _get_index_view(self, **kwargs):
        f = RequestFactory()
        params = urllib.parse.urlencode(kwargs)
        r = f.get(f'{reverse("hostlookup_combined:index")}?{str(params)}')
        r.user = User.objects.get_by_natural_key('networker')
        return HostLookupView.as_view()(r)

    @patch('hostlookup_combined.utils.lookup_cidr', mock_lookup_cidr_empty)
    def test_renders_form(self, views_get_connection, utils_get_connection, connections):
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

    def test_renders_form_selections(self, views_get_connection, utils_get_connection, connections):
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

    def test_renders_results(self, views_get_connection, utils_get_connection, connections):
        response = self._get_index_view(q='10.10.10.10', bluecat_config='1')
        response.render()
        self.assertContains(response, '<table')
        self.assertContains(response, '<th>IPv4</th>')
        self.assertContains(response, '141.100.0.0')
        # Renders order for IPv4 141.100.0.1
        self.assertContains(response, '<td class="valid" data-order="2372141057">')
        self.assertContains(response, 'example.com')
        self.assertContains(response, 'second.com')

    def test_renders_ip_error(self, views_get_connection, utils_get_connection, connections):
        response = self._get_index_view(q='foobar', bluecat_config='1')
        response.render()
        self.assertContains(response, 'does not appear to be an IPv4 or IPv6 address')

    def test_view_permission_required(self, views_get_connection, utils_get_connection, connections):
        response = self._get_index()
        self.assertEqual(response.status_code, 403)


class MergedCellTestCase(TestCase):
    def setUp(self):
        self.col_0 = MergedCell([], None)
        self.col_1 = MergedCell([SourceValue('ena', 'a')], None)
        self.col_valid = MergedCell([SourceValue('ena', 'a'), SourceValue('dio', 'a')], None)
        self.col_diff_types = MergedCell([SourceValue('ena', 1), SourceValue('dio', '1')], None)
        self.col_invalid = MergedCell([SourceValue('ena', 'a'), SourceValue('dio', 'b')], None)
        self.col_sort_len = MergedCell([SourceValue('ena', 'aaaaa')], len)
        self.col_sort_invalid = MergedCell([SourceValue('ena', 'aaaaa'), SourceValue('dio', 'bbbbb')], len)

    def test_different_invalid(self):
        self.assertFalse(self.col_invalid.valid)

    def test_same_valid(self):
        self.assertTrue(self.col_valid.valid)

    def test_single_valid(self):
        self.assertTrue(self.col_1.valid)

    def test_none_valid(self):
        self.assertTrue(self.col_0.valid)

    def test_diff_types_invalid(self):
        self.assertFalse(self.col_diff_types.valid)

    def test_sort_none(self):
        self.assertIs(self.col_valid.sort_order, None)

    def test_sort_len(self):
        self.assertIs(self.col_sort_len.sort_order, 5)

    def test_sort_invalid(self):
        self.assertIs(self.col_sort_invalid.sort_order, 0)

    def test_render_invalid(self):
        rendered = merged_cell(self.col_invalid)
        self.assertIn('<li>ena: a</li>', rendered)
        self.assertIn('<li>dio: b</li>', rendered)
        self.assertIn('invalid', rendered)

    def test_render_valid(self):
        rendered = merged_cell(self.col_valid)
        self.assertFalse('<li>' in rendered)
        self.assertFalse(':' in rendered)
        self.assertFalse('ena' in rendered)
        self.assertFalse('dio' in rendered)
        self.assertIn('class="valid"', rendered)
        self.assertIn('>a<', rendered)

    def test_render_sort_order_none(self):
        rendered = merged_cell(self.col_valid)
        self.assertFalse('data-order' in rendered)

    def test_render_sort_order_invalid(self):
        rendered = merged_cell(self.col_invalid)
        self.assertIn('data-order="0"', rendered)

    def test_render_sort_order_len(self):
        rendered = merged_cell(self.col_sort_len)
        self.assertIn('data-order="5"', rendered)


class MergedRowTestCase(TestCase):
    def setUp(self):
        self.data_1 = {
            'alpha': 1,
            'beta': 'two',
            'gamma': [0, 0, 0],
            'epsilon': 'e',
        }
        self.data_2 = {
            'alpha': 2,
            'beta': 'two',
            'gamma': [0, 0, 0],
            'delta': 'four',
        }
        self.merged = MergedRow(None, ena=self.data_1, dio=self.data_2)

    def test_single_source_all_valid(self):
        single_source = MergedRow(None, ena=self.data_1)
        self.assertTrue(single_source.cells['alpha'].valid)
        self.assertTrue(single_source.cells['beta'].valid)
        self.assertTrue(single_source.cells['gamma'].valid)
        self.assertTrue(single_source.cells['epsilon'].valid)

    def test_alpha_invalid(self):
        self.assertFalse(self.merged.cells['alpha'].valid)

    def test_beta_valid(self):
        self.assertTrue(self.merged.cells['beta'].valid)

    def test_gamma_valid(self):
        self.assertTrue(self.merged.cells['gamma'].valid)

    def test_delta_valid(self):
        self.assertTrue(self.merged.cells['delta'].valid)

    def test_epsilon_valid(self):
        self.assertTrue(self.merged.cells['epsilon'].valid)


class MergedTableTestCase(TestCase):
    def setUp(self):
        self.source_a = [
            {
                'id': 0,
                'color': 'green',
                'size': 5,
            },
            {
                'id': 1,
                'color': 'red',
                'size': 8,
            },
            {
                'id': 2,
                'color': 'red',
                'size': 7,
            },
            {
                'id': 3,
                'color': 'black',
                'size': 3,
            },
        ]
        self.source_b = [
            {
                'id': 0,
                'color': 'green',
                'size': 5,
            },
            {
                'id': 1,
                'color': 'yellow',
                'size': 5,
            },
            {
                'id': 4,
                'color': 'white',
                'size': 6,
            },
        ]
        self.source_c = [
            {
                'id': 0,
                'status': 'jolly',
            },
            {
                'id': 1,
                'status': 'despondent'
            },
        ]
        self.columns = [
            ('id', 'ID'),
            ('size', 'Size'),
            ('color', 'Color'),
            ('status', 'Status', len),
        ]

    def test_status_added(self):
        merged = MergedTable('id', self.columns, None, a=self.source_a, c=self.source_c)
        self.assertTrue('status' in merged.rows[0].cells.keys())
        self.assertTrue('status' in merged.rows[1].cells.keys())

    def test_outer_join(self):
        merged = MergedTable('id', self.columns, None, a=self.source_a, b=self.source_b)
        self.assertIs(len(merged.rows.values()), 5)

    def test_inner_join(self):
        merged = MergedTable('id', self.columns, ('a', 'b'), a=self.source_a, b=self.source_b)
        self.assertIs(len(merged.rows.values()), 2)

    def test_single_required(self):
        merged = MergedTable('id', self.columns, ('a'), a=self.source_a, b=self.source_b)
        self.assertTrue(merged.rows.get(0))
        self.assertTrue(merged.rows.get(3))
        self.assertIs(merged.rows.get(4), None)

    def test_column_sort_func(self):
        merged = MergedTable('id', self.columns, None, a=self.source_a, c=self.source_c)
        self.assertIs(merged.rows[0].cells['status'].sort_order, 5)

    def test_render(self):
        merged = MergedTable('id', self.columns, None, a=self.source_a, b=self.source_b)
        rendered = merged_table(merged, 'foo').replace('\n', '').replace('    ', '')
        self.assertIn('<table class="foo">', rendered)
        self.assertIn('<tr><th>ID</th>', rendered)
        self.assertIn('<tr class=""><td class="valid">', rendered)
