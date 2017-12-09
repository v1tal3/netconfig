from ...scripts_bank.lib import netmiko_functions as nfn
from ...scripts_bank.lib import functions as fn
from flask import g, session

class BaseDevice(object):
	ssh = {}

	def __init__(self, id, hostname, ipv4_addr, type, ios_type):
		self.id = id
		self.hostname = hostname
		self.ipv4_addr = ipv4_addr
		self.type = type
		self.ios_type = ios_type
		self.activeSession = self.retrieve_ssh_session()
		self.interface = ''

	def return_stored_ssh(self):
		return ssh

	def enter_config_mode(self):
		self.activeSession.config_mode()

	def exit_config_mode(self):
		self.activeSession.exit_config_mode()

	def run_ssh_command(self, command):
		return nfn.runSSHCommandInSession(command, self.activeSession)

	def run_ssh_config_commands(self, cmdList):
		return nfn.runMultipleSSHConfigCommandsInSession(cmdList, self.activeSession)

	def run_multiple_commands(self, command):
		newCmd = []
		for x in self.split_on_newline(command):
			newCmd.append(x)
		result = nfn.runMultipleSSHCommandsInSession(newCmd, self.activeSession)

	def run_multiple_config_commands(self, command):
		newCmd = []
		for x in self.split_on_newline(command):
			newCmd.append(x)
		# Get command output from network device
		result = nfn.runMultipleSSHConfigCommandsInSession(newCmd, self.activeSession)
		saveResult = self.save_config_on_device()
		for x in saveResult:
			result.append(x)
		return result

	# Splits string into an array by each newline ('\n') in string
	def split_on_newline(self, x):
		return fn.splitOnNewline(x)

	# Gets SSH command output and returns it as an array, with each line separated by a newline ('\n')
	def get_cmd_output(self, x):
		result = self.run_ssh_command(x)
		return self.split_on_newline(result)

	def replace_double_spaces_commas(self, x):
		return fn.replaceDoubleSpacesCommas(x)

	def find_prompt_in_session(self):
		return nfn.findPromptInSession(self.activeSession)

	# Returns active SSH session for provided host (self) if it exists.  Otherwise gets a session, stores it, and returns it
	def retrieve_ssh_session(self):
		user_id = str(g.db.hget('users', session['USER']))
		password = str(g.db.hget(str(user_id), 'pw'))
		creds = fn.setUserCredentials(session['USER'], password)
		#creds = fn.setUserCredentials(user, password)
		# Store SSH Dict key as self.id followed by '-' followed by username
		sshKey = str(self.id) + '--' + str(session['UUID'])

		#if not self.ssh[sshKey]:
		if sshKey not in self.ssh:
			fn.writeToLog('initiated new SSH connection to %s' % (self.hostname))
			# If no currently active SSH sessions, initiate a new one
			self.ssh[sshKey] = nfn.getSSHSession(self.ios_type, self.ipv4_addr, creds)
		
		# Run test to verify if socket connection is still open or not
		if not nfn.sessionIsAlive(self.ssh[sshKey]):
			# If session is closed, reestablish session and log event
			fn.writeToLog('reestablished SSH connection to %s' % (self.hostname))
			self.ssh[sshKey] = nfn.getSSHSession(self.ios_type, self.ipv4_addr, creds)

		self.activeSession = self.ssh[sshKey]
		return self.ssh[sshKey]
		