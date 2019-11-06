from django.test import TestCase

from .merge import MergedTable, MergedRow, MergedCell, SourceValue
from hostlookup_combined.templatetags.merge_tags import merged_table, merged_cell


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
