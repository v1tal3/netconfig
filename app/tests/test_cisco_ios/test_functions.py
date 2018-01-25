import unittest
from app.device_classes.device_definitions.cisco.cisco_ios import CiscoIOS


class TestCiscoIOS(unittest.TestCase):
    """CI testing class for Cisco IOS devices."""

    def setUp(self):
        """Initialize static class testing variables."""
        self.device = CiscoIOS('na', 'na', 'na', 'na', 'na', 'na')

        self.ios_output = """Interface              IP-Address      OK? Method Status                Protocol
        Vlan1                  192.168.0.1     YES DHCP   up                    up
        FastEthernet1/0/1      unassigned      YES NVRAM  up                    down
        FastEthernet1/0/2      unassigned      YES unset  down                  down
        FastEthernet1/0/3      unassigned      YES unset  administratively down down
        """

        self.ios_output_comparison = [{'status': 'up', 'name': 'Vlan1',
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

        self.cdp_neigh_input = ['Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID',
                                'router02         Fas 0/1           76                R    MikroTik  bridge1']

    def test_cleanup_ios_output(self):
        """Test IOS interface output cleanup function."""
        result = self.device.cleanup_ios_output(self.ios_output)

        assert result == self.ios_output_comparison

    def test_count_interface_status(self):
        """Test count_interface_status function."""
        count_interface_status_comparison = {'down': 2,
                                             'disabled': 1,
                                             'total': 4,
                                             'up': 1}

        result = self.device.count_interface_status(self.ios_output_comparison)
        assert result == count_interface_status_comparison

    def test_cdp_neighbor_formatting(self):

        cdp_neigh_comparison = [{'hold_time': '76', 'capability': 'R',
                                'platform': 'MikroTik', 'local_iface': 'Fas0/1',
                                'port_id': 'bridge1', 'device_id': 'router02'}]

        result = self.device.cleanup_cdp_neighbor_output(self.cdp_neigh_input)

        assert result == cdp_neigh_comparison
