from ..base_device import BaseDevice

class CiscoIOS(BaseDevice):
#class CiscoIosBaseDevice():
	# abc
	def get_run_config_cmd(self):
		command = 'show running-config'
		return command

	def get_start_config_cmd(self):
		command = 'show startup-config'
		return command

	def get_cdp_neighbor_cmd(self):
		command = 'show cdp neighbors | begin ID'
		return command