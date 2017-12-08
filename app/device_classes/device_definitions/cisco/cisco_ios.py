from ..base_device import BaseDevice

class CiscoIOS(BaseDevice):

	def get_run_config_cmd(self): #required
		command = 'show running-config'
		return command

	def get_start_config_cmd(self): #required
		command = 'show startup-config'
		return command

	def get_cdp_neighbor_cmd(self): #required
		command = 'show cdp neighbors | begin ID'
		return command

	def pull_interface_config(self):
		command = "show run interface %s | exclude configuration|!" % (self.interface)
		return self.split_on_newline(self.run_ssh_command(command))

	def pull_interface_mac_addresses(self):
		command = "show mac address-table interface %s" % (self.interface)
		for a in range(2):
			result = self.run_ssh_command(command)
			if self.check_invalid_input_detected(result):
				command = "show mac-address-table interface %s" % (self.interface)
				continue
			else:
				break
		if self.check_invalid_input_detected(result):
			return ''
		else:
			return self.split_on_newline(self.replace_double_spaces_commas(result).replace('*', ''))


	def check_invalid_input_detected(self, x):
		if "Invalid input detected" in x:
			return True
		else:
			return False

	def pull_interface_statistics(self):
		command = "show interface %s" % (self.interface)
		return self.split_on_newline(self.run_ssh_command(command))

	def pull_interface_info(self): #required
		intConfig = self.pull_interface_config()
		intMac = self.pull_interface_mac_addresses()
		intStats = self.pull_interface_statistics()

		return intConfig, intMac, intStats


