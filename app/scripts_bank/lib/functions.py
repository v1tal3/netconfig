#!/usr/bin/python

import logging
from app import app
from flask import session


class UserCredentials(object):
    """Stores interface authentication session results when searching for a client on the network."""

    def __init__(self, un, pw, priv):
        """Initialization method."""
        self.un = un
        self.pw = pw
        self.priv = priv


"""Global variables."""
# Credentials class variable.  Stores as creds.un and creds.pw for username and password
creds = UserCredentials('', '', '')

"""Global logging settings."""
# Syslogging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create a file handler
handler = logging.FileHandler(app.config['SYSLOGFILE'])
handler.setLevel(logging.INFO)
# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
# Add the handlers to the logger
logger.addHandler(handler)


def writeToLog(msg):
    """Write provided message to log file.

    Try/catch in case User isn't logged in, and Netconfig URL is access directly.
    """
    try:
        logger.info(session['USER'] + ' - ' + msg)
    except KeyError:
        logger.info('[unknown user] - ' + msg)


def setUserCredentials(username, password, privPassword=''):
    """Return creds class with username and password in it."""
    creds.un = username
    creds.pw = password
    creds.priv = privPassword
    return creds


def containsSkipped(x):
    """Return if the word 'skipped' is in the provided string.

    Returns True if string contains the word "skipped".
    Returns False otherwise.
    """
    try:
        if "skipped" in str(x):
            return True
        else:
            return False
    except:
        return False
