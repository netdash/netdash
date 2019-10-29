from django.test import TestCase

from .merge import MergedRow, MergedColumn, SourceValue


class MergedColumnTestCase(TestCase):
    def setUp(self):
        self.col_0 = MergedColumn([])
        self.col_1 = MergedColumn([SourceValue('ena', 'a')])
        self.col_valid = MergedColumn([SourceValue('ena', 'a'), SourceValue('dio', 'a')])
        self.col_diff_types = MergedColumn([SourceValue('ena', 1), SourceValue('dio', '1')])
        self.col_invalid = MergedColumn([SourceValue('ena', 'a'), SourceValue('dio', 'b')])

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
        self.assertTrue(single_source.columns['alpha'].valid)
        self.assertTrue(single_source.columns['beta'].valid)
        self.assertTrue(single_source.columns['gamma'].valid)
        self.assertTrue(single_source.columns['epsilon'].valid)

    def test_alpha_invalid(self):
        self.assertFalse(self.merged.columns['alpha'].valid)

    def test_beta_valid(self):
        self.assertTrue(self.merged.columns['beta'].valid)

    def test_gamma_valid(self):
        self.assertTrue(self.merged.columns['gamma'].valid)

    def test_delta_valid(self):
        self.assertTrue(self.merged.columns['delta'].valid)

    def test_epsilon_valid(self):
        self.assertTrue(self.merged.columns['epsilon'].valid)
