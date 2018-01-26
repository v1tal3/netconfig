import unittest
from app.device_classes.device_definitions.cisco.cisco_ios import CiscoIOS


class TestCiscoIOS(unittest.TestCase):
    """CI testing class for Cisco IOS devices."""

    def setUp(self):
        """Initialize static class testing variables."""
        self.device = CiscoIOS('na', 'na', 'na', 'na', 'na', 'na')

        self.ios_output = '''
Interface              IP-Address      OK? Method Status                Protocol
Vlan1                  192.168.0.1     YES DHCP   up                    up
FastEthernet1/0/1      unassigned      YES NVRAM  up                    down
FastEthernet1/0/2      unassigned      YES unset  down                  down
FastEthernet1/0/3      unassigned      YES unset  administratively down down
'''

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

        self.cdp_input_data = '''
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone,
                  D - Remote, C - CVTA, M - Two-port Mac Relay

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
ABC1234567890AB  Gig 1/0/10        124              H P   Polycom S Port 1
router01.DOMAIN.com
                 Fas 0/1           76                R    MikroTik  bridge1
DEF90AB12345678  Gig 4/0/37        130              H P   Polycom S Port 1
PC0A1.domain.com
                 Gig 3/0/11        174             T B I  C3560G    Gig 0
AP002
                 Gig 4/0/10        132             T B I  AIR-CAP35 Gig 1
Switch02-4A
                 Gig 2/0/37        145              S I   WS-C3560G Gig 0/1
STP567890AB1234  Gig 4/0/4         167              H P   Polycom S Port 1
        '''

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
        """Test IOS CDP neighbor output formatting."""
        expected_output = [{'hold_time': '124', 'capability': 'H P', 'platform': 'Polycom S', 'local_iface': 'Gig 1/0/10', 'port_id': 'Port 1', 'device_id': 'ABC1234567890AB'},
                           {'hold_time': '76', 'capability': 'R', 'platform': 'MikroTik', 'local_iface': 'Fas 0/1', 'port_id': 'bridge1', 'device_id': 'router01.DOMAIN.com'},
                           {'hold_time': '130', 'capability': 'H P', 'platform': 'Polycom S', 'local_iface': 'Gig 4/0/37', 'port_id': 'Port 1', 'device_id': 'DEF90AB12345678'},
                           {'hold_time': '174', 'capability': 'T B I', 'platform': 'C3560G', 'local_iface': 'Gig 3/0/11', 'port_id': 'Gig 0', 'device_id': 'PC0A1.domain.com'},
                           {'hold_time': '132', 'capability': 'T B I', 'platform': 'AIR-CAP35', 'local_iface': 'Gig 4/0/10', 'port_id': 'Gig 1', 'device_id': 'AP002'},
                           {'hold_time': '145', 'capability': 'S I', 'platform': 'WS-C3560G', 'local_iface': 'Gig 2/0/37', 'port_id': 'Gig 0/1', 'device_id': 'Switch02-4A'},
                           {'hold_time': '167', 'capability': 'H P', 'platform': 'Polycom S', 'local_iface': 'Gig 4/0/4', 'port_id': 'Port 1', 'device_id': 'STP567890AB1234'}]

        result = self.device.cleanup_cdp_neighbor_output(self.cdp_input_data.splitlines())

        self.assertEqual(result, expected_output)
