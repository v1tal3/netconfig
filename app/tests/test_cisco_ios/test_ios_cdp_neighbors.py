import unittest
from app.device_classes.device_definitions.cisco.cisco_ios import CiscoIOS


class TestCiscoIOS(unittest.TestCase):
    """CI testing class for Cisco IOS devices."""

    def setUp(self):
        """Initialize static class testing variables."""
        self.device = CiscoIOS('na', 'na', 'na', 'na', 'na', 'na')

        self.cdp_input_data = '''
-------------------------
Device ID: ABC1234567890AB
Entry address(es):
  IP address: 10.0.53.81
Platform: Polycom SoundPoint IP 123,  Capabilities: Host Phone
Interface: GigabitEthernet2/0/12,  Port ID (outgoing port): Port 1
Holdtime : 138 sec

Version :
Updater: 5.0.8, App: 4.0.8

advertisement version: 2
Duplex: full
Power drawn: 3.900 Watts

-------------------------
Device ID: AP01234
Entry address(es):
  IP address: 10.18.175.20
  IPv6 address: FE80::1234:5678:90AB  (link-local)
Platform: cisco AIR-CAP2702I-A-K9,  Capabilities: Trans-Bridge Source-Route-Bridge IGMP
Interface: GigabitEthernet5/0/25,  Port ID (outgoing port): FastEthernet0
Holdtime : 141 sec

Version :
Cisco IOS Software, C2700 Software (AP3G2-K9W8-M), Version 10.1(2)JA3, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2015 by Cisco Systems, Inc.
Compiled Mon 01-Jan-00 01:23 by prod_rel_team

advertisement version: 2
Duplex: full
Power drawn: 15.400 Watts
Power request id: 2367, Power management id: 2
Power request levels are:16800 15400 13000 0 0
Management address(es):
  IP address: 10.18.175.20

-------------------------
Device ID: PC0A1.domain.com
Entry address(es):
  IP address: 192.168.14.44
Platform: cisco WS-C6509-32,  Capabilities: Router Switch IGMP
Interface: FastEthernet4/0/5,  Port ID (outgoing port): bridge1
Holdtime : 131 sec

Version :
Cisco IOS Software, Catalyst 6500 L3 Switch  Software (cat6500e-UNIVERSALK9-M), Version 10.1(2)E3, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2016 by Cisco Systems, Inc.
Compiled Mon 01-Jan-00 01:23 by prod_rel_team

advertisement version: 2
VTP Management Domain: 'domainA1'
Native VLAN: 1
Duplex: full
Management address(es):
  IP address: 192.168.14.44

-------------------------
Device ID: Switch02-4A
Entry address(es):
  IP address: 172.18.95.111
Platform: cisco WS-C2960XR-32,  Capabilities: Router Switch IGMP
Interface: TenGigabitEthernet2/0/5,  Port ID (outgoing port): GigabitEthernet1/1/19
Holdtime : 163 sec

Version :
Cisco IOS Software, Catalyst 2960 L3 Switch  Software (cat2900e-UNIVERSALK9-M), Version 10.1(2)E3, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2016 by Cisco Systems, Inc.
Compiled Mon 01-Jan-00 01:23 by prod_rel_team

advertisement version: 2
VTP Management Domain: 'VTP_123-45C'
Native VLAN: 1
Duplex: full
Management address(es):
  IP address: 172.18.95.111
'''

    def test_ios_cdp_neighbor_formatting(self):
        """Test IOS CDP neighbor output formatting."""
        expected_output = [{'local_iface': 'Gig 2/0/12', 'port_id': 'Port 1', 'hold_time': '124', 'platform': 'Polycom SoundPoint IP 123', 'device_id': 'ABC1234567890AB', 'remote_ip': '10.0.53.81'},
                           {'local_iface': 'Gig 5/0/25', 'port_id': 'Fas 0', 'hold_time': '76', 'platform': 'cisco AIR-CAP2702I-A-K9', 'device_id': 'AP01234', 'remote_ip': '10.18.175.20'},
                           {'local_iface': 'Fas 4/0/5', 'port_id': 'bridge1', 'hold_time': '130', 'platform': 'cisco WS-C6509-32', 'device_id': 'PC0A1.domain.com', 'remote_ip': '192.168.14.44'},
                           {'local_iface': 'Ten 2/0/5', 'port_id': 'Gig 1/1/19', 'hold_time': '174', 'platform': 'cisco WS-C2960XR-32', 'device_id': 'Switch02-4A', 'remote_ip': '172.18.95.111'}]

        actual_output = self.device.cleanup_cdp_neighbor_output(self.cdp_input_data.splitlines())

        for x, y in zip(expected_output, actual_output):
            self.assertEqual(x['local_iface'], y['local_iface'])
            self.assertEqual(x['port_id'], y['port_id'])
            self.assertEqual(x['platform'], y['platform'])
            self.assertEqual(x['device_id'], y['device_id'])
            self.assertEqual(x['remote_ip'], y['remote_ip'])
