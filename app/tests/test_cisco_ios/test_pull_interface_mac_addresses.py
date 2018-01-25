import unittest
from app.device_classes.device_definitions.cisco.cisco_ios import CiscoIOS
try:
    import mock
except ImportError:
    from unittest import mock


class TestCiscoIOS(unittest.TestCase):
    """CI testing class for Cisco IOS devices."""

    @mock.patch.object(CiscoIOS, 'run_ssh_command')
    def test_pull_interface_mac_addresses(self, mocked_method):
        """Test MAC address table formatting."""
        device = CiscoIOS('na', 'na', 'na', 'na', 'na', 'na')
        # This needs to be defined for the test
        device.interface = None

        mocked_method.return_value = '''
                  Mac Address Table
        -------------------------------------------

        Vlan    Mac Address       Type        Ports
        ----    -----------       --------    -----
           1    1234.5678.90ab    DYNAMIC     Po1
          10    90ab.1234.5678    DYNAMIC     Gi1/0/1
         100    5678.90ab.1234    DYNAMIC     Po100
        '''

        ios_expected_output = [{'macAddr': '1234.5678.90ab', 'port': 'Po1', 'vlan': '1'},
                               {'macAddr': '90ab.1234.5678', 'port': 'Gi1/0/1', 'vlan': '10'},
                               {'macAddr': '5678.90ab.1234', 'port': 'Po100', 'vlan': '100'}]

        self.assertEqual(device.pull_interface_mac_addresses(None), ios_expected_output)
