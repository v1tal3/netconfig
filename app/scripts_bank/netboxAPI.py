from app import app
import requests


class NetboxHost(object):
    """Class for storing device information pulled from Netbox via API calls."""

    def __init__(self, id, hostname, ipv4_addr, type, ios_type):
        """Initilization method."""
        self.id = id
        self.hostname = hostname
        self.ipv4_addr = ipv4_addr
        self.type = type
        self.ios_type = ios_type


def getDeviceType(x):
    """Input type of device (network, database, server, etc), returns ID in Netbox database."""
    r = requests.get(app.config['NETBOXSERVER'] + '/api/dcim/device-roles/')

    if r.status_code == requests.codes.ok:
        for device in r.json()['results']:
            if device['name'] == x:
                return device['id']
    else:
        return False


def getDeviceTypeOS(x):
    """Get Device Type of specific Netbox Device ID"""
    r = requests.get(app.config['NETBOXSERVER'] + '/api/dcim/device-types/' + str(x))

    if r.status_code == requests.codes.ok:

        # NOTE should probably put a try/catch around this
        netconfigOS = r.json()['custom_fields']['Netconfig_OS']['label']

        if netconfigOS == 'IOS':
            return 'cisco_ios'
        elif netconfigOS == 'IOS-XE':
            return 'cisco_xe'
        elif netconfigOS == 'NX-OS':
            return 'cisco_nxos'
        elif netconfigOS == 'ASA':
            return 'cisco_asa'
        else:  # Default to simply cisco_ios
            return 'cisco_ios'

    else:

        # NOTE should this be False?
        return 'cisco_ios'


def getHostByID(x):
    """Return host info in same format as SQLAlchemy responses, for X-Compatibility with local DB choice.

    x is host ID
    """

    r = requests.get(app.config['NETBOXSERVER'] + '/api/dcim/devices/' + str(x))

    if r.status_code == requests.codes.ok:
        data = r.json()
        return NetboxHost(str(x), data['name'],
                          data['primary_ip']['address'].split('/', 1)[0],
                          data['device_type']['model'],
                          # can we get this in the previous response?
                          getDeviceTypeOS(data['device_type']['id']))

    else:
        return None


def getHosts():
    """Return all devices stored in Netbox."""

    r = requests.get(app.config['NETBOXSERVER'] + '/api/dcim/devices/?limit=0')

    if r.status_code == requests.codes.ok:

        # NOTE probably don't need to strip primary_ip cidr.
        # Not seeing this as a problem connecting
        result = [host for host in r.json()['results']
                  if host['custom_fields']['Netconfig'] and
                  host['custom_fields']['Netconfig']['label'] == 'Yes']

        return result

    else:

        return None


def getHostID(x):
    """Input device name/hostname, returns id as stored in Netbox."""
    r = requests.get(app.config['NETBOXSERVER'] + '/api/dcim/devices/?limit=0')

    if r.status_code == requests.codes.ok:

        for host in r.json()['results']:
            if host['display_name'] == x:  # Network
                return host['id']

    else:

        return None


def getHostName(x):
    """Input ID, return device name from Netbox."""
    r = requests.get(app.config['NETBOXSERVER'] + '/api/dcim/devices/' + str(x))

    if r.status_code == requests.codes.ok:

        # TODO add try/catch here
        return r.json()['name']

    else:

        return None


def getHostIPAddr(x):
    """Input ID, return device IP address from Netbox."""
    r = requests.get(app.config['NETBOXSERVER'] + '/api/dcim/devices/' + str(x))

    if r.status_code == requests.codes.ok:

        # TODO add try/catch here
        return r.json()['primary_ip']['address'].split('/', 1)[0]

    else:

        return None


def getHostType(x):
    """Input ID, return device type from Netbox."""
    r = requests.get(app.config['NETBOXSERVER'] + '/api/dcim/devices/' + str(x))

    if r.status_code == requests.codes.ok:

        # TODO add try/catch here
        return r.json()['device_type']['model']

    else:

        return None
