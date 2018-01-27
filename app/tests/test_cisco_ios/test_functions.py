import unittest
from app.device_classes.device_definitions.cisco.cisco_ios import CiscoIOS


class TestCiscoIOS(unittest.TestCase):
    """CI testing class for Cisco IOS devices."""

    def setUp(self):
        """Initialize static class testing variables."""
        self.device = CiscoIOS('na', 'na', 'na', 'na', 'na', 'na')

        self.interface_input_data = '''
Interface              IP-Address      OK? Method Status                Protocol
Vlan1                  192.168.0.1     YES DHCP   up                    up
FastEthernet1/0/1      unassigned      YES NVRAM  up                    down
FastEthernet1/0/2      unassigned      YES unset  down                  down
FastEthernet1/0/3      unassigned      YES unset  administratively down down
'''

        self.interface_expected_output = [{'status': 'up', 'name': 'Vlan1',
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
DEF90AB12345678  Gig 4/0/37        130              H P   Polycom   Port 2
PC0A1.domain.com
                 Gig 3/0/11        174             T B I  C3560G    Gig 0
AP002
                 Gig 4/0/10        132             T B I  AIR-CAP35 Gig 1
Switch02-4A
                 Gig 2/0/37        145              S I   WS-C3560G Gig 0/1
STP567890AB1234  Gig 4/0/4         167             H P M  IP Phone  Port 1
        '''

    def test_cleanup_ios_output(self):
        """Test IOS interface output cleanup function."""
        actual_output = self.device.cleanup_ios_output(self.interface_input_data)

        self.assertEqual(actual_output, self.interface_expected_output)

    def test_count_interface_status(self):
        """Test count_interface_status function."""
        count_interface_status_comparison = {'down': 2,
                                             'disabled': 1,
                                             'total': 4,
                                             'up': 1}

        actual_output = self.device.count_interface_status(self.interface_expected_output)
        self.assertEqual(actual_output, count_interface_status_comparison)

    def test_ios_cdp_neighbor_formatting(self):
        """Test IOS CDP neighbor output formatting."""
        expected_output = [{'local_iface': 'Gig 1/0/10', 'port_id': 'Port 1', 'hold_time': '124', 'platform': 'Polycom', 'device_id': 'ABC1234567890AB'},
                           {'local_iface': 'Fas 0/1', 'port_id': 'bridge1', 'hold_time': '76', 'platform': 'MikroTik', 'device_id': 'router01.DOMAIN.com'},
                           {'local_iface': 'Gig 4/0/37', 'port_id': 'Port 2', 'hold_time': '130', 'platform': 'Polycom', 'device_id': 'DEF90AB12345678'},
                           {'local_iface': 'Gig 3/0/11', 'port_id': 'Gig 0', 'hold_time': '174', 'platform': 'C3560G', 'device_id': 'PC0A1.domain.com'},
                           {'local_iface': 'Gig 4/0/10', 'port_id': 'Gig 1', 'hold_time': '132', 'platform': 'AIR-CAP35', 'device_id': 'AP002'},
                           {'local_iface': 'Gig 2/0/37', 'port_id': 'Gig 0/1', 'hold_time': '145', 'platform': 'WS-C3560G', 'device_id': 'Switch02-4A'},
                           {'local_iface': 'Gig 4/0/4', 'port_id': 'Port 1', 'hold_time': '167', 'platform': 'IP Phone', 'device_id': 'STP567890AB1234'}]

        # Sort so tests always line up
        actual_output = self.device.cleanup_cdp_neighbor_output(self.cdp_input_data.splitlines())

        for x, y in zip(expected_output, actual_output):
            self.assertEqual(x['local_iface'], y['local_iface'])
            self.assertEqual(x['port_id'], y['port_id'])
            self.assertEqual(x['hold_time'], y['hold_time'])
            self.assertEqual(x['platform'], y['platform'])
            self.assertEqual(x['device_id'], y['device_id'])
