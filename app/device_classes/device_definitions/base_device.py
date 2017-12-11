from ...scripts_bank.lib import netmiko_functions as nfn
from ...scripts_bank.lib import functions as fn
from flask import g, session

class BaseDevice(object):

	def __init__(self, id, hostname, ipv4_addr, type, ios_type):
		self.id = id
		self.hostname = hostname
		self.ipv4_addr = ipv4_addr
		self.type = type
		self.ios_type = ios_type

	def __del__(self):
		pass

	def return_stored_ssh(self):
		return sshStore

	def enter_config_mode(self, activeSession):
		nfn.runEnterConfigModeInSession(activeSession)

	def exit_config_mode(self, activeSession):
		nfn.runExitConfigModeInSession(activeSession)

	def run_ssh_command(self, command, activeSession):
		return nfn.runSSHCommandInSession(command, activeSession)

	def run_ssh_config_commands(self, cmdList, activeSession):
		return nfn.runMultipleSSHConfigCommandsInSession(cmdList, activeSession)

	def run_multiple_commands(self, command, activeSession):
		newCmd = []
		for x in self.split_on_newline(command):
			newCmd.append(x)
		result = nfn.runMultipleSSHCommandsInSession(newCmd, activeSession)

	def run_multiple_config_commands(self, command, activeSession):
		newCmd = []
		for x in self.split_on_newline(command):
			newCmd.append(x)
		# Get command output from network device
		result = nfn.runMultipleSSHConfigCommandsInSession(newCmd, activeSession)
		saveResult = self.save_config_on_device(activeSession)
		for x in saveResult:
			result.append(x)
		return result

	# Splits string into an array by each newline ('\n') in string
	def split_on_newline(self, x):
		return fn.splitOnNewline(x)

	# Gets SSH command output and returns it as an array, with each line separated by a newline ('\n')
	def get_cmd_output(self, command, activeSession):
		result = self.run_ssh_command(command, activeSession)
		return self.split_on_newline(result)

	def get_cmd_output_with_commas(self, command, activeSession):
		result = self.run_ssh_command(command, activeSession)
		result = self.replace_double_spaces_commas(result)
		return self.split_on_newline(result)

	def replace_double_spaces_commas(self, x):
		return fn.replaceDoubleSpacesCommas(x)

	def find_prompt_in_session(self, activeSession):
		return nfn.findPromptInSession(activeSession)
	'''
	# Returns active SSH session for provided host (self) if it exists.  Otherwise gets a session, stores it, and returns it
	def retrieve_ssh_session(self):
		user_id = str(g.db.hget('users', session['USER']))
		password = str(g.db.hget(str(user_id), 'pw'))
		creds = fn.setUserCredentials(session['USER'], password)
		# Store SSH Dict key as self.id followed by '-' followed by username
		sshKey = str(self.id) + '--' + str(session['UUID'])

		#if not self.sshStore[sshKey]:
		if sshKey not in type(self).sshStore:
			fn.writeToLog('initiated new SSH connection to %s' % (self.hostname))
			# If no currently active SSH sessions, initiate a new one
			type(self).sshStore[sshKey] = nfn.getSSHSession(self.ios_type, self.ipv4_addr, creds)
		
		# Run test to verify if socket connection is still open or not
		if not nfn.sessionIsAlive(type(self).sshStore[sshKey]):
			# If session is closed, reestablish session and log event
			fn.writeToLog('reestablished SSH connection to %s' % (self.hostname))
			type(self).sshStore[sshKey] = nfn.getSSHSession(self.ios_type, self.ipv4_addr, creds)

		self.activeSession = type(self).sshStore[sshKey]
		return self.activeSession
	'''
