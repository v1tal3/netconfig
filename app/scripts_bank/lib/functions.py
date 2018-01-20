#!/usr/bin/python

import re
import socket
import sys
import os
import errno
import hashlib
import logging
import netmiko_functions as nfn
from app import app
from datetime import datetime
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
    except:
        logger.info('[unknown user] - ' + msg)


def debugScript(x):
    """For debugging purposes only."""
    print x
    sys.exit()


def debugErrorOut(num):
    """For debugging purposes only."""
    print "Error with script: #%s" % (num)
    print "Locals:"
    print locals()
    print "\nGlobals:"
    print globals()
    sys.exit()


def debugDict(d):
    """For debugging purposes only.

    Prints all contents of dictionary for debugging purposes.
    """
    for k, v in d.iteritems():
        print k, v


def setUserCredentials(username, password, privPassword=''):
    """Return creds class with username and password in it."""
    creds.un = username
    creds.pw = password
    creds.priv = privPassword
    return creds


def rreplace(s, old, new, occurrence):
    """Replace last occurence of character in string.

    s is string original string.
    old is the character to be replaced.
    new is the character to be used instead of old character.
    occurence is how many occurrence's to replace, starting from the end.
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)


def indexLookup(x):
    """Index lookup for determining Cisco IOS type.

    This needs to be cleaned up and standardized for multiple vendors.
    Returns index of -1 or -2, as IOS-XE/NX-OS has a trailing whitespace at the end of strings.
    This helps determine if a string came from IOS or IOS-XE/NX-OS.
    """
    if x:
        # Index of last variable in command output.  -1 if IOS
        return int('-1')
    else:
        # Index of last variable in command output.  -2 if IOS-XE or NX-OS
        return int('-2')


def file_len(fname):
    """Return number of items (lines) in a file as an integer."""
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def textBlock_len(x):
    """Return number of items (lines) in a given block of text."""
    i = 0
    for a in x:
        i += 1
    return i


def countCharOccurences(x, y):
    """Return number of occurences of a given character in provided string.

    x = the string to check against.
    y = the character to check for in the string.
    """
    return x.count(y)


def errorCheckEmptyIncResult(x):
    """Check if variable is empty or Incomplete.

    If variable is empty or contains an Incomplete entry, return True.
    Otherwise return False.
    """
    if not x or ("Inc" in x):
        return True
    else:
        return False


def isEmpty(x):
    """Check if variable is empty.

    If variable is empty, return True.
    Otherwise return False.
    """
    if not x:
        return True
    else:
        return False


def isSkipped(x):
    """Check if string contains 'skipped', for SSH sessions failing.

    If variable equals 'skipped', return True.
    Otherwise return False.
    """
    if x == 'skipped':
        return True
    else:
        return False


def containsSkipped(x):
    """Return if the word 'skipped' is in the provided string.

    Returns True if string contains the word "skipped".
    Returns False otherwise.
    """
    try:
        if "skipped" in str(x):
            return True
        return False
    except:
            return False


def isInt(x):
    """Check if value entered is a integer.

    Checks if x is an integer.
    Returns True if it is.
    Returns False if it isn't.
    """
    try:
        int(x)
        return True
    except ValueError:
        return False


def removeDictKey(d, key):
    """Remove key from dictionary."""
    r = dict(d)
    del r[key]
    return r


def getCurrentTime():
    """Get current timestamp for when starting a script."""
    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return currentTime


def getScriptRunTime(startTime):
    """Return time elapsed between current time and provided time in 'startTime'."""
    endTime = getCurrentTime() - startTime
    return endTime


def makeDirectory(path):
    """Make directory, throw error if it doesn't work."""
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def printProgress(iteration, total, prefix='', suffix='', decimals=2, barLength=100):
    """Print iterations progress to terminal.

    Call in a loop to create terminal progress bar
    @params:
    iteration      - Required  : current iteration (Int)
        total      - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
    """
    filledLength = int(round(barLength * iteration / float(total)))
    percents = round(100.00 * (iteration / float(total)), decimals)
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('%s [%s] %s%s %s  (%s/%s total)\r' % (prefix, bar, percents, '%', suffix, iteration, total))
    sys.stdout.flush()
    if iteration == total:
        print("\n")


def findLineInConfig(config, searchTerm):
    """Return line with specified text in provided config."""
    for item in config.split("\n"):
        if searchTerm in item:
            return item.strip()


def findLineAfterLineInConfig(config, startTerm, searchTerm):
    """Return the next line found following the specfied starting line.

    Example: Find the IP address (searchTerm) after interface Serial0/0/0 (startTerm).
    """
    t = False
    for item in config.split("\n"):
        if t:
            if searchTerm in item:
                return item.strip()
        if startTerm in item:
            t = True
    # If term isn't found, return empty value.
    # Function should return a value before this triggers.
    return ''


def readFromFile(inputFileName):
    """Read and return all contents from a file."""
    # Open file provided by user to import list of store numbers from
    fileRead = open(inputFileName, 'r')
    # Read each line of the file into array fileLines
    fileLines = fileRead.readlines()
    # Close this file once import is completed
    fileRead.close()
    # Return contents
    return fileLines


def writeCommandToFile(command, filename):
    """Write string/command to new file.  Doesn't append."""
    fileWrite = open(filename, 'wb')
    fileWrite.write(command)
    fileWrite.close()


def appendCommandToFile(command, filename):
    """Append string/command to new/existing file."""
    fileWrite = open(filename, 'ab')
    fileWrite.write(command)
    fileWrite.close()


def convertMacFormatDec2Col(oldMac):
    """Convert decimal notation MAC address into all uppercase colon delimited format.

    Example: inputting 1234.56ab.cdef returns 12:34:56:AB:CD:EF.
    """
    # Strip any newlines from string
    oldMac = oldMac.strip()
    # Check var length.  If not equal to 14, return originally provided address.  Otherwise continue with conversion
    if len(oldMac) == 14:
        # Counter for 'for' loop
        i = 0
        # Set newMac var to null
        newMac = ''
        # Insert a colon after every 2nd character
        for char in oldMac:
            # Skip if character is a decimal
            if char != ".":
                # Append the character to the newMac string
                newMac += str(char)
                # Increment counter
                i += 1
            else:
                # Reset counter to 0
                i = 0
            # Check if remainder is 0, if so insert colon. Don't insert colon if at the end of the list
            if (i % 2 == 0) and (i > 0):
                newMac += ":"
        # Return converted MAC address in colon delimited format
        return newMac[:-1].upper()
    else:
        # Incorrect MAC format imported
        return oldMac


def convertMacFormatCol2Dec(oldMac):
    """Convert MAC address format with colons or hyphens to Cisco's decimal format.

    Converts uppercase or lowercase colon or hyphen delimited format MAC address into all lowercase decimal notation
    Example: inputting 12:34:56:AB:CD:EF returns 1234.56ab.cdef.
    """
    # Strip any newlines from string
    oldMac = oldMac.strip()
    # Verify MAC address formatting is correct for colon or hyphen delimited format
    if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", oldMac.lower()):
        # Counter for 'for' loop
        i = 0
        # Set newMac var to null
        newMac = ''
        # Insert a decimal after every 4th character
        for char in oldMac:
            # Set skip variable if MAC address is colon delimited
            if macFormatType(oldMac) == 'c':
                skipVar = ':'
            # Set skip variable if MAC address is hyphen delimited
            elif macFormatType(oldMac) == 'h':
                skipVar = '-'

            if char != skipVar:
                # Append the character to the newMac string
                newMac += str(char)
                # Increment counter
                i += 1
            # Check if remainder is 0, if so insert colon. Don't insert colon if at the end of the list
            if (i % 4 == 0) and (i > 0):
                # Insert decimal into string every fourth character
                newMac += "."
                # Reset counter to 0
                i = 0
        # Return converted MAC address in decimal delimited format
        return newMac[:-1].lower()
    else:
        # Incorrect MAC format imported
        return oldMac


def convertMacFormatText2Dec(oldMac):
    """Convert MAC address format from text to Cisco's decimal format.

    Converts uppercase or lowercase text only (no deliminations) formatted MAC address into all lowercase decimal notation
    Example: inputting 123456ABCDEF returns 1234.56ab.cdef
    """
    # Strip any newlines from string
    oldMac = oldMac.strip()
    # Verify MAC address formatting is correct for colon or hyphen delimited format
    if re.match("[0-9a-f]{12}$", oldMac.lower()):
        # Counter for 'for' loop
        i = 0
        # Set newMac var to null
        newMac = ''
        # Insert a decimal after every 4th character
        for char in oldMac:
            # Append the character to the newMac string
            newMac += str(char)
            # Increment counter
            i += 1
            # Check if remainder is 0, if so insert colon. Don't insert colon if at the end of the list
            if (i % 4 == 0) and (i > 0):
                # Insert decimal into string every fourth character
                newMac += "."
                # Reset counter to 0
                i = 0
        # Return converted MAC address in decimal delimited format
        return newMac[:-1].lower()
    else:
        # Incorrect MAC format imported
        return oldMac


def macFormatType(mac):
    """Determine MAC address format.

    Return 'c' for colon delimited format.
    Return 'h' for hypen delimted format.
    Return 'd' for decimal delimited format.
    Return 't' for text format (no delimiters).
    Return 'e' if no other matches.
    """
    # Regex expression for colon delimited format with 12 characters exactly
    if re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
        return 'c'
    # Regex expression for hypen delimited format with 12 characters exactly
    elif re.match("[0-9a-f]{2}([-])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
        return 'h'
    # Regex expression for decimal delimited format with 12 characters exactly
    elif re.match("[0-9a-f]{4}([.])[0-9a-f]{4}([.])[0-9a-f]{4}$", mac.lower()):
        return 'd'
    # Regex expression for text only format with no separators
    elif re.match("[0-9a-f]{12}$", mac.lower()):
        return 't'
    # Return 'e' if all checks above fail
    else:
        return 'e'


def md5(fname):
    """Determine MD5 checksum of file.

    Return MD5 checksum string.
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def removeCharFromString(oldString, character):
    """Remove all instances of a provided character from a string, then returns string."""
    newString = oldString.replace(character.strip(), '')
    return newString


def getFileSize(imageFileFullPath):
    """Return size of file in bytes."""
    size = os.path.getsize(imageFileFullPath)
    return int(size)


def reverseDNSEndpoint(host):
    """Try to lookup endpoint name via reverse DNS.

    Returns IP address provided if it fails.
    """
    try:
        # Try host lookup via reverse DNS
        hostNameList = socket.gethostbyaddr(host)
    except socket.error, v:
        # If it fails, return as a generic Endpoint
        return host
    # Return hostname of IP address from reverse DNS lookup
    return hostNameList[0].split("'")[0]


def md5VerifyOnDeviceWithSession(command, child):
    """Return true if verification succeeds, otherwise return false."""
    md5VerifyResult = nfn.runSSHCommandInSession(command, child)

    # Run for each line retreived from the md5 verification output
    for result in md5VerifyResult.split("\n"):

        # TODO investigate just result.split()
        resultList = [x.strip() for x in result.split("  ")]

        # If first word in string is 'Verified', then it worked
        if resultList[0] == "Verified":
            return True
        # If first word in string is '%Error' and second word is 'verifying', it failed
        elif resultList[0] == "%Error" and resultList[1] == "verifying":
            return False
        # Continue loop until one of the two above triggers
        else:
            continue
