import re
from ..cisco_base_device import CiscoBaseDevice


class CiscoIOS(CiscoBaseDevice):
    """Class for IOS type devices from vendor Cisco."""

    def cmd_run_config(self):
        """Return command to display running configuration on device."""
        command = 'show running-config'
        return command

    def cmd_start_config(self):
        """Return command to display startup configuration on device."""
        command = 'show startup-config'
        return command

    def cmd_cdp_neighbor(self):
        """Return command to display CDP/LLDP neighbors on device."""
        command = "show cdp neighbors | begin ID"
        return command

    def pull_run_config(self, activeSession):
        """Retrieve running configuration on device."""
        command = self.cmd_run_config()
        return self.get_cmd_output(command, activeSession)

    def pull_start_config(self, activeSession):
        """Retrieve startup configuration on device."""
        command = self.cmd_start_config()
        return self.get_cmd_output(command, activeSession)

    def pull_cdp_neighbor(self, activeSession):
        """Retrieve CDP/LLDP neighbor information from device."""
        command = self.cmd_cdp_neighbor()
        result = self.get_cmd_output(command, activeSession)
        return self.cleanup_cdp_neighbor_output(result)

    def pull_interface_config(self, activeSession):
        """Retrieve configuration for interface on device."""
        command = "show run interface %s | exclude configuration|!" % (self.interface)
        return self.get_cmd_output(command, activeSession)

    def pull_interface_mac_addresses(self, activeSession):
        """Retrieve MAC address table for interface on device."""
        command = "show mac address-table interface %s" % (self.interface)
        for a in range(2):
            result = self.run_ssh_command(command, activeSession)
            if self.check_invalid_input_detected(result):
                command = "show mac-address-table interface %s" % (self.interface)
                continue
            else:
                break
        if self.check_invalid_input_detected(result):
            return '', ''
        else:
            # Stores table headers as string
            tableHeader = ''
            # Stores table body data as array
            tableBody = []

            # Remove any asterisks
            result = result.replace('*', '')

            # In IOS-XE, there are multiple protocols separated by commas.
            # Separate these by underscores instead to preserve formatting in HTML output
            result = result.replace(',', '_')
            result = self.replace_double_spaces_commas(result).splitlines()

            for index, line in enumerate(result):
                # This is primarily for IOS-XE devices.  We only want Unicast Entries
                # We want to stop output once we reach Multicast Entries
                if 'Unicast Entries' in line:
                    # Do not store this line as output
                    pass
                elif 'Multicast Entries' in line:
                    # We are done with Unicast entries, so break out of loop
                    break
                # Loop until header is filled, as the header isn't always in the very first line
                elif not tableHeader and ',' in line:
                    # Skip this iteration if there's only a single comma.  The header should have multiple fields
                    if line.count(',') > 1:
                        # Store table header line in string, with commas to separate fields
                        tableHeader = line
                elif line and 'Mac' not in line and '-' not in line:
                    # Regexp to search for any substring in line that contains an underscore.
                    # Then replaces the whitespace around it with commas.
                    # This is for IOS-XE devices with multiple protocols that interface with HTML formatting.
                    regExp = re.compile(r'\s[a-zA-Z0-9]*_[a-zA-Z0-9_]*\s')
                    if regExp.search(line):
                        # Save matched string to variable
                        regexMatchList = regExp.findall(line)
                        # Strip first and last character (whitespace) of string
                        regexMatchStr = regexMatchList[0][1:-1]
                        # Add commas back in to beginning and end of line
                        regexMatchStr = ',' + regexMatchStr + ','
                        # Insert modified substring back into line
                        line = re.sub(regExp, regexMatchStr, line)

                    # Remove any single spaces in front of commas
                    line = line.replace(' ,', ',')
                    tableBody.append(line)

            return tableHeader, tableBody

    def pull_interface_statistics(self, activeSession):
        """Retrieve statistics for interface on device."""
        command = "show interface %s" % (self.interface)
        return self.get_cmd_output(command, activeSession)

    def pull_interface_info(self, activeSession):
        """Retrieve various informational command output for interface on device."""
        intConfig = self.pull_interface_config(activeSession)
        intMacHead, intMacBody = self.pull_interface_mac_addresses(activeSession)
        intStats = self.pull_interface_statistics(activeSession)

        return intConfig, intMacHead, intMacBody, intStats

    def pull_device_uptime(self, activeSession):
        """Retrieve device uptime."""
        command = 'show version | include uptime'
        return self.get_cmd_output(command, activeSession).split("is")[1]

    def pull_host_interfaces(self, activeSession):
        """Retrieve list of interfaces on device."""
        result = self.run_ssh_command('show ip interface brief', activeSession)

        return self.cleanup_ios_output(result)

    def count_interface_status(self, interfaces):
        """Return count of interfaces.

        Up is total number of up/active interfaces.
        Down is total number of down/inactive interfaces.
        Disable is total number of administratively down/manually disabled interfaces.
        """
        data = {}
        data['up'] = data['down'] = data['disabled'] = 0

        for x in interfaces:
            if 'up' in x['status']:
                data['up'] += 1
            elif 'down' in x['status']:
                data['down'] += 1
            elif 'administratively' in x['status']:
                data['disabled'] += 1

        return data
