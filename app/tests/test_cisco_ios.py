import unittest
from app.device_classes.device_definitions.cisco.cisco_ios import CiscoIOS


class TestCiscoIOS(unittest.TestCase):

    def setUp(self):

        self.device = CiscoIOS('na', 'na', 'na', 'na', 'na', 'na')

        self.ios_output = """Interface              IP-Address      OK? Method Status                Protocol
        Vlan1                  192.168.2.250   YES DHCP   up                    up
        FastEthernet0/1        unassigned      YES unset  up                    up
        FastEthernet0/2        unassigned      YES unset  administratively                  down
        """

    def test_cleanup_ios_output(self):

        comparison = [{'status': 'up', 'ok': 'YES', 'name': 'Vlan1',
                       'address': '192.168.2.250', 'protocol': 'up',
                       'method': 'DHCP'},
                      {'status': 'up', 'ok': 'YES', 'name': 'FastEthernet0/1',
                       'address': 'unassigned', 'protocol': 'up',
                       'method': 'unset'},
                      {'status': 'administratively', 'ok': 'YES',
                       'name': 'FastEthernet0/2', 'address': 'unassigned',
                       'protocol': 'down', 'method': 'unset'}]

        assert self.device.cleanup_ios_output(self.ios_output) == comparison

    def test_count_interface_status(self):

        cleanup_output = self.device.cleanup_ios_output(self.ios_output)

        comparision = {'down': 0, 'disabled': 1, 'up': 2}

        assert self.device.count_interface_status(cleanup_output) == comparision
