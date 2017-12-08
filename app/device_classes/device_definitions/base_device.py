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
		self.activesession = self.retrieve_ssh_session()
		self.interface = ''

	def return_stored_ssh(self):
		return ssh

	def run_ssh_command(self, command):
		return nfn.runSSHCommandInSession(command, self.activesession)

	def run_ssh_config_commands(self, commands):
		return nfn.runMultipleSSHConfigCommandsInSession(commands, self.activesession)

	def run_multiple_commands(self, command):
		newCmd = []
		for x in self.split_on_newline(command):
			newCmd.append(x)
		result = nfn.runMultipleSSHCommandsInSession(newCmd, self.activesession)

	def run_multiple_config_commands(self, command):
		newCmd = []
		for x in self.split_on_newline(command):
			newCmd.append(x)
		# Get command output from network device
		result = nfn.runMultipleSSHConfigCommandsInSession(newCmd, self.activesession)
		saveResult = self.save_config_on_device()
		for x in saveResult:
			result.append(x)
		return result

	def split_on_newline(self, output):
		return output.split('\n')

	def replace_double_spaces_commas(self, x):
		return fn.replaceDoubleSpacesCommas(x)

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

	    return self.ssh[sshKey]
		