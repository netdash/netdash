from django.test import TestCase

from .merge import MergedTable, MergedRow, MergedCell, SourceValue


class MergedCellTestCase(TestCase):
    def setUp(self):
        self.col_0 = MergedCell([])
        self.col_1 = MergedCell([SourceValue('ena', 'a')])
        self.col_valid = MergedCell([SourceValue('ena', 'a'), SourceValue('dio', 'a')])
        self.col_diff_types = MergedCell([SourceValue('ena', 1), SourceValue('dio', '1')])
        self.col_invalid = MergedCell([SourceValue('ena', 'a'), SourceValue('dio', 'b')])

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
        self.merged = MergedRow(ena=self.data_1, dio=self.data_2)

    def test_single_source_all_valid(self):
        single_source = MergedRow(ena=self.data_1)
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

    def test_status_added(self):
        merged = MergedTable('id', a=self.source_a, c=self.source_c)
        self.assertTrue('status' in merged.columns)
        self.assertTrue('status' in merged.rows[0].cells.keys())
        self.assertTrue('status' in merged.rows[1].cells.keys())

    def test_extra_rows(self):
        merged = MergedTable('id', a=self.source_a, b=self.source_b)
        self.assertTrue(len(merged.rows.values()) == 5)
