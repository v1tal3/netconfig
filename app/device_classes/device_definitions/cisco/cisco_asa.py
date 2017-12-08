from ..base_device import BaseDevice

class CiscoASA(BaseDevice):
#class CiscoIosBaseDevice():
	# abc
	def get_run_config_cmd(self):
		command = 'show running-config'
		return command

	def get_start_config_cmd(self):
		command = 'show startup-config'
		return command

	# Command not supported on Cisco ASA
	def get_cdp_neighbor_cmd(self):
		command = ''
		return command