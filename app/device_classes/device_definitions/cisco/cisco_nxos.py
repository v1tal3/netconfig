from ..base_device import BaseDevice

class CiscoNXOS(BaseDevice):
#class CiscoIosBaseDevice():
	# abc
	def get_run_config_cmd(self):
		command = 'show running-config | exclude !'
		return command

	def get_start_config_cmd(self):
		command = 'show startup-config | exclude !'
		return command

	def get_cdp_neighbor_cmd(self):
		command = 'show cdp neighbors | begin ID'
		return command