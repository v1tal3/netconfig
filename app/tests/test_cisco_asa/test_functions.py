import unittest
from app.device_classes.device_definitions.cisco.cisco_asa import CiscoASA


class TestCiscoASA(unittest.TestCase):
    """CI testing class for Cisco ASA devices."""

    def setUp(self):
        """Initialize static class testing variables."""
        self.device = CiscoASA('na', 'na', 'na', 'na', 'na', 'na')

        self.asa_output = """Interface              IP-Address      OK? Method Status                Protocol
        Vlan1                  192.168.0.1     YES DHCP   up                    up
        FastEthernet1/0/1      unassigned      YES NVRAM  up                    down
        FastEthernet1/0/2      unassigned      YES unset  down                  down
        FastEthernet1/0/3      unassigned      YES unset  administratively down down
        """

        self.asa_output_comparison = [{'status': 'up', 'name': 'Vlan1',
                                       'address': '192.168.0.1', 'protocol': 'up',
                                       'method': 'DHCP'},
                                      {'status': 'up', 'name': 'FastEthernet1/0/1',
                                       'address': 'unassigned', 'protocol': 'down',
                                       'method': 'NVRAM'},
                                      {'status': 'down', 'name': 'FastEthernet1/0/2',
                                       'address': 'unassigned', 'protocol': 'down',
                                       'method': 'unset'},
                                      {'status': 'administratively', 'name': 'FastEthernet1/0/3',
                                       'address': 'unassigned', 'protocol': 'down',
                                       'method': 'unset'}]

    def test_cleanup_asa_output(self):
        """Test ASA interface output cleanup function."""
        assert self.device.cleanup_ios_output(self.asa_output) == self.asa_output_comparison

    def test_count_interface_status(self):
        """Test count_interface_status function."""
        count_interface_status_comparison = {'down': 2, 'disabled': 1, 'total': 4, 'up': 1}
        assert self.device.count_interface_status(self.asa_output_comparison) == count_interface_status_comparison

    def test_pull_interface_mac_addresses(self):
        """Test pull_interface_mac_addresses function."""
        asa_expected_output = ''
        self.assertEqual(self.device.pull_interface_mac_addresses(None), asa_expected_output)
