import json
import xmltodict

from pyovm.utils.xmlrpclib import ServerProxy

class Linux(object):
    def __init__(self, dst):
        self.dst = dst
        self.srv_raw_data = None
        self.server = None
        self.hardware = None
        self.phy_luns = None
        self.mounted_fs = None
        self.repos = None
        self.pkgs = None
        self.boot_time = None
        self.datetime = None
        self.timezone = None
        self.log = None
        
        """
        'discover_server',                         !!!
        'discover_hardware',                       !!!
        'discover_physical_luns',                  !!!
        'discover_mounted_file_systems',           !!!
        'package_get_repositories',                !!!
        'package_list',                            !!!
        'get_system_disk_space',                   !!!
        'get_last_boot_time',                      !!!
        'get_ntp',                                 !!!
        'get_datetime',                            !!!
        'get_timezone'                             !!!
        'get_log',                                 !!!
        """
        
        #print("[Linux] %s" % self.uri)
        self.conn = ServerProxy(self.uri, verbose=0)
    
    @property
    def uri(self):
        uri = "https://%s:%s@%s:%s/RPC2" % (self.dst.admin_name,
                                            self.dst.admin_pswd,
                                            self.dst.host,
                                            self.dst.port)
        return uri

    def __xml_postprocessor(self, path, key, value):
        return (key.lower(), value)

    def discover_server(self):
        try:
            r = self.conn.discover_server()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], basestring)):
                s='<?xml version'
                if s in r[0]:
                    d = xmltodict.parse(xml_input=r[0],
                                        xml_attribs=True,
                                        process_namespaces=True,
                                        postprocessor=self.__xml_postprocessor)
                    p1 = 'discover_server_result'
                    p2 = 'server'
                    data = d[p1][p2]
                    self.server = Server(data)
                    return self.server
                else:
                    #print json.dumps(d, indent=4)
                    raise Exception("Failed to parse data in response")
            else:
                print json.dumps(r[0], indent=4)
                raise Exception("Failed to parse data in response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def discover_hardware(self):
        try:
            r = self.conn.discover_hardware()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], basestring)):
                s='<?xml version'
                if s in r[0]:
                    d = xmltodict.parse(xml_input=r[0],
                                        xml_attribs=True,
                                        process_namespaces=True,
                                        postprocessor=self.__xml_postprocessor)
                    p1 = 'discover_hardware_result'
                    p2 = 'nodeinformation'
                    data = d[p1][p2]
                    self.hardware = Hardware(data)
                    return self.hardware
                else:
                    #print json.dumps(d, indent=4)
                    raise Exception("Failed to parse data in response")
            else:
                print json.dumps(r[0], indent=4)
                raise Exception("Failed to parse data in response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def discover_physical_luns(self):
        pass

    def discover_mounted_file_systems(self):
        pass

    def package_get_repositories(self):
        pass

    def package_list(self):
        pass

    def get_system_disk_space(self):
        pass

    def get_last_boot_time(self):
        pass

    def get_ntp(self):
        pass

    def get_datetime(self):
        pass

    def get_timezone(self):
        pass

    def get_log(self):
        pass

    def to_json(self):
        """ Returns JSON representation of this object. """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)

class Server(Linux):
    """ 'discover_server'!!!"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

    '''
    def to_json(self):
        """ Returns JSON representation of this object. """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)
    '''

class Hardware(Linux):
    """'discover_hardware'!!!"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

class PhysicalLuns(Linux):
    """'discover_physical_luns'!!!"""
    def __init__(self):
        pass

class MountedFileSystems(Linux):
    """'discover_mounted_file_systems'!!!"""
    def __init__(self):
        pass

class Repositories(Linux):
    """'package_get_repositories'!!!"""
    def __init__(self):
        pass

class Packages(Linux):
    """'package_list'!!!"""
    def __init__(self):
        pass

class DiskSpace(Linux):
    """'get_system_disk_space'!!!"""
    def __init__(self):
        pass

class BootTime(Linux):
    """'get_last_boot_time'!!!"""
    def __init__(self):
        pass

class NTP(Linux):
    """'get_ntp'!!!"""
    def __init__(self):
        pass

class DateTime(Linux):
    """'get_datetime'!!!"""
    def __init__(self):
        pass

class TimeZone(Linux):
    """'get_timezone'!!!"""
    def __init__(self):
        pass

class Log(Linux):
    """'get_log'!!!"""
    def __init__(self):
        pass




