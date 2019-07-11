from django.test import TestCase


class DummyTest(TestCase):

    def test_dummy(self):
        self.assertEqual(1, 1, msg="Example Devices SNMP")
