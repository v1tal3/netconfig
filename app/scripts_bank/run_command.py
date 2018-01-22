#!/usr/bin/python

import lib.netmiko_functions as nfn


def getCmdOutput(ssh, command):
    """Get command output from host by provided IP address."""
    output = []

    # Get command output from network device
    result = nfn.runSSHCommandInSession(command, ssh)

    # Split output by newline
    output = result.splitlines()

    # Return config
    return output


def getCmdOutputNoCR(ssh, command):
    """Get command output from host by provided IP address without submitting a Carriage Return at the end."""
    return nfn.runSSHCommandInSessionNoCR(command, ssh).splitlines()


def getCfgCmdOutput(ssh, command):
    """Get configuration command output from host by provided IP address."""
    output = []

    # Get configuration command output from network device
    result = nfn.runSSHCfgCommandInSession(command, ssh)

    # Split output by newline
    output = result.splitlines()

    # Remove first item in list, as Netmiko returns the command ran only in the output
    output.pop(0)

    # Return config
    return output
