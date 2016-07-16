import time
import json
import xmltodict

from pyovm.utils.xmlrpclib import ServerProxy

class Linux(object):
    def __init__(self, dst):
        self.dst = dst
        self.srv_raw_data = None
        self.server = None
        self.hardware = None

        self.phy_luns = []
        self.scsi_disks = []
        self.scsi_targets = []

        self.mounted_fs = []
        self.repos = {}

        self.pkgs_installed = []
        self.pkgs_updates = []

        self.sys_disk_space = None

        self.boot_time = None

        self.ntp = None

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
                    raise Exception("Failed to parse data from response")
            else:
                print json.dumps(r[0], indent=4)
                raise Exception("Failed to parse data from response")
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
                    raise Exception("Failed to parse data from response")
            else:
                print json.dumps(r[0], indent=4)
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def discover_physical_luns(self):
        """'discover_physical_luns'!!!"""
        try:
            r = self.conn.discover_physical_luns('',)
            assert(isinstance(r, tuple))
            if(isinstance(r[0], basestring)):
                s='<?xml version'
                if s in r[0]:
                    d = xmltodict.parse(xml_input=r[0],
                                        xml_attribs=True,
                                        process_namespaces=True,
                                        postprocessor=self.__xml_postprocessor)
                    p1 = 'discover_physical_luns_result'
                    p2 = 'scsi'
                    p3 = 'disk'
                    data = d[p1]
                    scsi_disk_data = data.get(p2).get(p3)
                    if scsi_disk_data:
                        for item in scsi_disk_data:
                            obj = SCSIDisc(item)
                            self.scsi_disks.append(obj)
                    p4 = 'iscsi_target'
                    scsi_target_data = data.get(p4)
                    if scsi_target_data:
                        for item in scsi_target_data:
                            obj = SCSITarget(item)
                            self.scsi_targets.append(obj)
                    
                            #print json.dumps(item, indent=4)
                else:
                    #print json.dumps(d, indent=4)
                    raise Exception("Failed to parse data from response")
            else:
                print json.dumps(r[0], indent=4)
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def discover_mounted_file_systems(self):
        """'discover_mounted_file_systems'!!!"""
        try:
            r = self.conn.discover_mounted_file_systems("all")
            assert(isinstance(r, tuple))
            if(isinstance(r[0], basestring)):
                s='<?xml version'
                if s in r[0]:
                    d = xmltodict.parse(xml_input=r[0],
                                        xml_attribs=True,
                                        process_namespaces=True,
                                        postprocessor=self.__xml_postprocessor)
                    p1 = 'discover_mounted_file_systems_result'
                    p2 = 'filesystem'
                    data = d[p1][p2]
                    if(isinstance(data, list)):
                        # print json.dumps(data, indent=4)
                        for item in data:
                            fs = MountedFileSystem(item)
                            self.mounted_fs.append(fs)
                        return self.mounted_fs
                    else:
                        raise Exception("Failed to parse data from response")
                else:
                    #print json.dumps(d, indent=4)
                    raise Exception("Failed to parse data from response")
            else:
                print json.dumps(r[0], indent=4)
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def package_get_repositories(self):
        """'package_get_repositories'!!!"""
        try:
            r = self.conn.package_get_repositories()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], dict)):
                self.repos = Repositories(r[0])
                return self.repos
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def package_list(self, scope):
        """'package_list'!!!"""
        assert(scope is 'installed' or scope is 'updates')
        try:
            r = self.conn.package_list(scope)
            assert(isinstance(r, tuple))
            if(isinstance(r[0], list)):
                for e in r[0]:
                    pkg = Package(e)
                    if scope is 'installed':
                        self.pkgs_installed.append(pkg)
                    else:
                        self.pkgs_updates.append(pkg)
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def get_system_disk_space(self):
        """'get_system_disk_space'!!!"""
        try:
            r = self.conn.get_system_disk_space()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], dict)):
                self.sys_disk_space = DiskSpace(r[0])
                return self.sys_disk_space
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def get_last_boot_time(self):
        """'get_last_boot_time'!!!"""
        try:
            r = self.conn.get_last_boot_time()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], dict)):
                self.boot_time = BootTime(r[0])
                return self.boot_time
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def get_ntp(self):
        """'get_ntp'!!!"""
        try:
            r = self.conn.get_ntp()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], list)):
                self.ntp = NTP(r[0])
                return self.ntp
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def get_datetime(self):
        """'get_datetime'!!!"""
        try:
            r = self.conn.get_datetime()
            assert(isinstance(r, tuple))

            if(isinstance(r[0], list)):
                self.datetime = DateTime(r[0])
                return self.datetime
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def get_timezone(self):
        """'get_timezone'!!!"""
        pass

    def get_log(self):
        """'get_log'!!!"""
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

'''
class PhysicalLUNs(Linux):
    """'discover_physical_luns'!!!"""
    def __init__(self):
        self.scsi_disks = []
        pass
'''

class SCSIDisc(Linux):
    """'discover_physical_luns'!!!"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        print self.to_json()

class SCSITarget(Linux):
    """'discover_physical_luns'!!!"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        print self.to_json()

class MountedFileSystem(Linux):
    """'discover_mounted_file_systems'!!!"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

class Repositories(Linux):
    """'package_get_repositories'!!!"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

class Package(Linux):
    """'package_list'!!!"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

class DiskSpace(Linux):
    """'get_system_disk_space'!!!"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

class BootTime(Linux):
    """'get_last_boot_time'!!!"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

    def boot_time(self):
        if self.last_boot_time:
            return time.strftime('%m/%d/%Y %H:%M:%S',
                                 time.localtime(float(self.last_boot_time)))

    def current_time(self):
        if self.local_time:
            return time.strftime('%m/%d/%Y %H:%M:%S',
                                 time.localtime(float(self.local_time)))

class NTP(Linux):
    """'get_ntp'!!!"""
    def __init__(self, data):
        self.ntp_servers = data[0]
        self.local_time_source = data[1]
        self.is_ntp_running = data[2]
        #print self.to_json()

class DateTime(Linux):
    """'get_datetime'!!!"""
    def __init__(self, data):
        self.year = data[0]
        self.month = data[1]
        self.date = data[2]
        self.hour = data[3]
        self.min = data[4]
        self.sec = data[5]
        #print self.to_json()

    def to_str(self):
        s = "%s/%s/%s %s:%s:%s" % (self.month, self.date, self.year,
                                   self.hour, self.min, self.sec)
        return s

class TimeZone(Linux):
    """'get_timezone'!!!"""
    def __init__(self):
        pass

class Log(Linux):
    """'get_log'!!!"""
    def __init__(self):
        pass




