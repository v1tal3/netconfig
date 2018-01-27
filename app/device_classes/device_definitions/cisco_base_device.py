from base_device import BaseDevice
from app.scripts_bank.lib.functions import isInteger
import re


class CiscoBaseDevice(BaseDevice):
    """Base class for network device vendor Cisco."""

    def check_invalid_input_detected(self, x):
        """Check for invalid input when executing command on device."""
        if "Invalid input detected" in x:
            return True
        else:
            return False

    def get_cmd_enter_configuration_mode(self):
        """Return command for entering configuration mode."""
        command = "config term"
        return command

    def get_cmd_exit_configuration_mode(self):
        """Return command for exiting configuration mode."""
        command = "end"
        return command

    def get_cmd_enable_interface(self):
        """Return command for enabling interface on device."""
        command = "no shutdown"
        return command

    def get_cmd_disable_interface(self):
        """Return command for disabling interface on device."""
        command = "shutdown"
        return command

    def cleanup_ios_output(self, iosOutput):
        """Clean up returned IOS output from 'show ip interface brief'."""
        data = []

        for line in iosOutput.splitlines():
            try:
                x = line.split()
                if x[0] == "Interface":
                    continue
                else:
                    interface = {}
                    interface['name'] = x[0]
                    interface['address'] = x[1]
                    interface['method'] = x[3]
                    interface['status'] = x[4]
                    interface['protocol'] = x[5]
                    data.append(interface)
            except IndexError:
                continue

        return data

    def cleanup_nxos_output(self, nxosOutput):
        """Clean up returned NX-OS output from 'show ip interface brief'."""
        # TODO cleanup like cleanup_ios_output
        data = []

        for line in nxosOutput.splitlines():
            if line:
                x = line.split(',')
                try:
                    interface = {}
                    interface['name'] = x[0]
                    interface['address'] = x[1]
                    interface['description'] = x[2]
                    interface['method'] = ''
                    interface['protocol'] = x[3]
                    interface['status'] = self.get_interface_status(x[3])
                    data.append(interface)
                except IndexError:
                    continue

        return data

    def run_enable_interface_cmd(self, interface, activeSession):
        """Enable interface on device using existing SSH session."""
        cmdList = []
        cmdList.append("interface %s" % interface)
        cmdList.append("%s" % (self.get_cmd_enable_interface()))
        cmdList.append("end")

        return self.run_ssh_config_commands(cmdList, activeSession)

    def run_disable_interface_cmd(self, interface, activeSession):
        """Disable interface on device using existing SSH session."""
        cmdList = []
        cmdList.append("interface %s" % interface)
        cmdList.append("%s" % (self.get_cmd_disable_interface()))
        cmdList.append("end")

        return self.run_ssh_config_commands(cmdList, activeSession)

    def get_save_config_cmd(self):
        """Return command for saving configuration settings on device."""
        if self.ios_type == 'cisco_nxos':
            return "copy running-config startup-config"
        else:
            return "write memory"

    def save_config_on_device(self, activeSession):
        """Return command for saving configuration settings on device."""
        command = self.get_save_config_cmd()
        return self.run_ssh_command(command, activeSession).splitlines()

    def run_edit_interface_cmd(self, interface, datavlan, voicevlan, other, activeSession):
        """Edit interface on device with specified parameters on existing SSH session."""
        cmdList = []
        cmdList.append("interface %s" % interface)

        if datavlan != '0':
            cmdList.append("switchport access vlan %s" % datavlan)
        if voicevlan != '0':
            cmdList.append("switchport voice vlan %s" % voicevlan)
        if other != '0':
            # + is used to represent spaces
            other = other.replace('+', ' ')

            # & is used to represent new lines
            for x in other.split('&'):
                cmdList.append(x)

        cmdList.append("end")

        return self.run_ssh_config_commands(cmdList, activeSession)

    def cmd_show_inventory(self):
        """Return command to display device inventory."""
        command = 'show inventory'
        return command

    def cmd_show_version(self):
        """Return command to display device version."""
        command = 'show version'
        return command

    def pull_inventory(self, activeSession):
        """Pull device inventory.

        Pulls device inventory.
        Returns output as array with each new line on a separate row.
        """
        command = self.cmd_show_inventory()
        return self.run_ssh_command(command, activeSession).splitlines()

    def pull_version(self, activeSession):
        """Pull device version.

        Pulls device version.
        Returns output as array with each new line on a separate row.
        """
        command = self.cmd_show_version()
        return self.run_ssh_command(command, activeSession).splitlines()

    def cleanup_cdp_neighbor_output(self, result):
        """Clean up returned 'show cdp neighbor' output."""
        data = []
        # Temporarily stores each body string when device hostname is on its own line
        singleHostname = ''
        skipHeader = True

        for line in result:
            try:
                x = line.split()
                if "Device" in x[0]:
                    skipHeader = False
                    continue
                elif skipHeader:
                    continue
                # This is needed in case the hostname is too long and is returned on its own line
                elif ' ' not in line:
                    singleHostname += str(line)
                else:
                    if singleHostname:
                        x.insert(0, singleHostname)
                        singleHostname = ''
                    # Remove the Capabilities category by stripping any single-letter fields
                    regex = re.compile(r'\b[A-Z]{1}\b')
                    x = filter(lambda i: not regex.search(i), x)
                    # Assign items to dictionary
                    interface = {}
                    interface['device_id'] = x[0]
                    interface['local_iface'] = x[1] + ' ' + x[2]
                    interface['hold_time'] = x[3]
                    # interface['capability'] = x[4]
                    if len(x) == 6:
                        interface['platform'] = x[4]
                        interface['port_id'] = x[5]
                    elif len(x) == 7:
                        if '/' in x[-1] or isInteger(x[-1]):
                            interface['platform'] = x[-3]
                            interface['port_id'] = x[-2] + ' ' + x[-1]
                        else:
                            interface['platform'] = x[-3] + ' ' + x[-2]
                            interface['port_id'] = x[-1]
                    elif len(x) == 8:
                        interface['platform'] = x[4] + ' ' + x[5]
                        interface['port_id'] = x[6] + ' ' + x[7]
                    data.append(interface)
            except IndexError:
                continue

        return data
