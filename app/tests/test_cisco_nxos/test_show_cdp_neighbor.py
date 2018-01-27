import unittest
from app.device_classes.device_definitions.cisco.cisco_nxos import CiscoNXOS
try:
    import mock
except ImportError:
    from unittest import mock


class TestCiscoNXOS(unittest.TestCase):
    """CI testing class for Cisco NXOS devices."""

    @mock.patch.object(CiscoNXOS, 'run_ssh_command')
    def test_cdp_neighbor_formatting(self, mocked_method):
        """Test CDP neighbor formatting."""
        device = CiscoNXOS('na', 'na', 'na', 'na', 'na', 'na')

        mocked_method.return_value = '''
<?xml version="1.0" encoding="ISO-8859-1"?>
<nf:rpc-reply xmlns:nf="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="http://www.cisco.com/nxos:1.0:cdpd">
 <nf:data>
  <show>
   <cdp>
    <neighbors>
     <__XML__OPT_Cmd_show_cdp_neighbors_detail___readonly__>
      <__readonly__>
       <TABLE_cdp_neighbor_detail_info>
        <ROW_cdp_neighbor_detail_info>
         <ifindex>83886080</ifindex>
         <device_id>Switch-DC-1.domain.com(ABC123456DE)</device_id>
         <sysname>Switch-DC-1</sysname>
         <numaddr>1</numaddr>
         <v4addr>10.0.0.1</v4addr>
         <platform_id>N5K-C5548UP</platform_id>
         <capability>switch</capability>
         <capability>IGMP_cnd_filtering</capability>
         <capability>unknown enum:&lt;10&gt;</capability>
         <intf_id>Ethernet1/1</intf_id>
         <port_id>Ethernet1/1</port_id>
         <ttl>131</ttl>
         <version>Cisco Nexus Operating System (NX-OS) Software, Version 1.2(3)N4(5)</version>
         <version_no>v2</version_no>
         <mtu>1500</mtu>
         <syslocation>Data Center 1</syslocation>
         <num_mgmtaddr>1</num_mgmtaddr>
         <v4mgmtaddr>10.0.1.1</v4mgmtaddr>
        </ROW_cdp_neighbor_detail_info>
        <ROW_cdp_neighbor_detail_info>
         <ifindex>436207616</ifindex>
         <device_id>Switch-DC-2.domain.com(AB1234D)</device_id>
         <sysname>Switch-DC-2</sysname>
         <numaddr>1</numaddr>
         <v4addr>10.0.0.2</v4addr>
         <platform_id>N5K-C5548UP</platform_id>
         <capability>switch</capability>
         <capability>IGMP_cnd_filtering</capability>
         <capability>unknown enum:&lt;10&gt;</capability>
         <intf_id>Ethernet1/2</intf_id>
         <port_id>Ethernet1/2</port_id>
         <ttl>131</ttl>
         <version>Cisco Nexus Operating System (NX-OS) Software, Version 1.2(3)N4(5)</version>
         <version_no>v2</version_no>
         <nativevlan>2</nativevlan>
         <duplexmode>full</duplexmode>
         <mtu>1</mtu>
         <syslocation>Data Center 2</syslocation>
         <num_mgmtaddr>1</num_mgmtaddr>
         <v4mgmtaddr>10.0.1.2</v4mgmtaddr>
        </ROW_cdp_neighbor_detail_info>
       </TABLE_cdp_neighbor_detail_info>
      </__readonly__>
     </__XML__OPT_Cmd_show_cdp_neighbors_detail___readonly__>
    </neighbors>
   </cdp>
  </show>
 </nf:data>
</nf:rpc-reply>
'''

        expected_output = [{'local_iface': 'Ethernet1/1', 'platform': 'N5K-C5548UP',
                            'port_id': 'Ethernet1/1', 'device_id': 'Switch-DC-1'},
                           {'local_iface': 'Ethernet1/2', 'platform': 'N5K-C5548UP',
                            'port_id': 'Ethernet1/2', 'device_id': 'Switch-DC-2'}]

        self.assertEqual(device.pull_cdp_neighbor(None), expected_output)
