#!/usr/bin/python

import socket
import netmiko as nm


def sessionIsAlive(ssh):
    """Determine if stored Netmiko SSH session is established and active."""
    null = chr(0)
    try:
        # Try sending ASCII null byte to maintain the connection alive
        ssh.write_channel(null)
        return True
    except (socket.error, EOFError):
        # If unable to send, we can tell for sure that the connection is unusable
        return False
    return False


def sshSkipCheck(x):
    """Determine if SSH connection attempt was skipped from Netmiko.

    Returns True if SSH session contains "skipped" (was unsuccessful).
    Returns False otherwise.
    """
    if "skipped" in str(x):
        return True
    else:
        return False


def connectToSSH(host, creds):
    """Connect to host via SSH with provided username and password, and type of device specified."""
    # Try to connect to the host
    try:
        if creds.priv:
            ssh = nm.ConnectHandler(device_type=host.ios_type.strip(), ip=host.ipv4_addr.strip(), username=creds.un, password=creds.pw, secret=creds.priv)
            # Enter into enable mode
            ssh.enable()
        else:
            ssh = nm.ConnectHandler(device_type=host.ios_type.strip(), ip=host.ipv4_addr.strip(), username=creds.un, password=creds.pw)

    # except nm.AuthenticationException:
    #    return "%s skipped - authentication error\n" % (host)
    except:
        return "%s skipped - connection timeout\n" % (host)
    # Returns active SSH session to host
    return ssh


def disconnectFromSSH(ssh):
    """Disconnect from active SSH session."""
    try:
        if ssh:
            # Disconnect from the host
            ssh.disconnect()
    except:
        pass


def runSSHCommandOnce(command, host, creds):
    """Run command on host via SSH and returns output."""
    ssh = connectToSSH(host, creds)
    # Verify ssh connection established and didn't return an error
    if sshSkipCheck(ssh):
        return False
    # Get command output from device
    result = ssh.send_command(command)
    # Disconnect from SSH session
    disconnectFromSSH(ssh)
    # Return output of command
    return result


def runMultipleSSHCommandsWithCmdHead(cmdList, host, creds):
    """Run multiple commands on host via SSH and returns output."""
    result = []
    ssh = connectToSSH(host, creds)
    # Verify ssh connection established and didn't return an error
    if sshSkipCheck(ssh):
        return False
    for x in cmdList:
        result.append("Command: %s" % x)
        # Get command output from multiple commands configured on device
        result.append(ssh.send_command(x))
    # Disconnect from SSH session
    disconnectFromSSH(ssh)
    # Return output of command
    return result


def runMultipleSSHCommandsInSession(cmdList, ssh):
    """Run multiple commands in list on host via SSH and returns all output from applying the config."""
    result = []
    for x in cmdList:
        result.append("Command: %s" % x)
        # Get command output from multiple commands configured on device
        result.append(ssh.send_command(x))
    # Return output of command
    return result


def getSSHSession(host, creds):
    """Create an SSH session, verifies it worked, then returns the session itself."""
    ssh = connectToSSH(host, creds)
    # Verify ssh connection established and didn't return an error
    if sshSkipCheck(ssh):
        return "ERROR: In function nfn.getSSHSession, sshSkipCheck failed using host %s\n" % (host.hostname)
    # Return output of command
    return ssh


def runSSHCommandInSession(command, ssh):
    """Run command on provided existing SSH session and returns output."""
    # Return output of command
    return ssh.send_command(command)


def runSSHCommandInSessionNoCR(command, ssh):
    """Run command on provided existing SSH session and returns output.

    Since we set normalie to False, we need to do this.
    The normalize() function in NetMiko does rstrip and adds a CR to the end of the command.
    """
    # Return output of command
    return ssh.send_command(command.strip(), normalize=False)


def runSSHCfgCommandInSession(command, ssh):
    """Run config command on provided existing SSH session and returns output."""
    # Return output of command, omitting any lines with just the command displayed only (just how netmiko works with config commands)
    return ssh.send_config_set(command, exit_config_mode=False)


def runSSHCfgCommandInSessionNoCR(command, ssh):
    """Run config command on provided existing SSH session without a carraige return and returns output.

    Since we set normalie to False, we need to do this.
    The normalize() function in NetMiko does rstrip and adds a CR to the end of the command.
    """
    # Get command output from device
    # Return output of command, omitting any lines with just the command displayed only (just how netmiko works with config commands)
    return ssh.send_config_set(command, exit_config_mode=False)


def runEnterConfigModeInSession(ssh):
    """Enter configuration mode on provided existing SSH session and returns output."""
    # Return output of command
    return ssh.config_mode()


def runExitConfigModeInSession(ssh):
    """Exit configuration mode on provided existing SSH session and returns output."""
    # Get command output from device
    return ssh.exit_config_mode()


def runMultipleSSHConfigCommandsInSession(cmdList, ssh):
    """Run multiple commands in list on host via SSH and returns all output from applying the config."""
    # Get command output from multiple commands configured on device
    return ssh.send_config_set(cmdList).splitlines()


def findPromptInSession(ssh):
    """Get prompt from host."""
    return ssh.find_prompt()
