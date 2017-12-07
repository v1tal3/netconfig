class BaseDevice(object):
    def __init__(self, id, hostname, ipv4_addr, type, ios_type):
        self.id = id
        self.hostname = hostname
        self.ipv4_addr = ipv4_addr
        self.type = type
        self.ios_type = ios_type
